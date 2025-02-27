use crate::{
    attestation::{
        ATTESTATION_CERT_URL, ATTESTATION_PROVIDER_URL, AzureSgxAttestationRequest, Header,
        JsonWebKeySet, JwtResponse, RawJsonWebKeySet, SGX_ATTESTATION_URI, TEST_SIGNATURE,
        TokenClaims, validate_json_web_token,
    },
    constants::{
        ADDRESS_BYTE_LEN, COMPRESSED_KEY_BYTE_LEN, CUSTODIAN_ADDRESS_BYTE_LEN,
        SEAL_DATA_BUFFER_SIZE,
    },
    enclave::ecall::{
        ecall_get_encryption_key, ecall_get_registration_report, ecall_get_signing_address,
        ecall_get_user_data, ecall_init_diagnostics, ecall_init_sealed,
    },
    node::db::KEY_NODE_ID,
    types::{
        identifiers::{OperatorNodeId, ReleaseHash},
        primitives::{Bytes32, CompressedKey, CustodianAddress, FixedBytesWrapper},
        state::{SealedData, SealedDataKey},
    },
    util::enclave::ReleaseMeasurement,
};
use anyhow::{Result, bail, ensure};
use base64::Engine;
use deadpool_postgres::{Pool, Transaction};
use ethereum_types::Address;
use rustc_hex::ToHex;
use sgx_types::{
    error::SgxStatus,
    types::{AttributesFlags, EnclaveId, QuoteNonce, Report, TargetInfo},
};
use sgx_urts::enclave::SgxEnclave;
use sha2::{Digest, Sha256};
use std::{
    self,
    collections::HashMap,
    path::{Path, PathBuf},
    str,
    thread::sleep,
    time::Duration,
};

pub mod ecall;
pub mod ocall_impl;
pub mod runtime;

/// Use 8k buffer to fit large DCAP quote
const RET_QUOTE_BUF_LEN: u32 = 8192;

#[repr(C)]
pub struct SGXQuoteC {
    pub qe_report: Report,
    pub ti: TargetInfo,
    pub quote_nonce: QuoteNonce,
    pub quote_len: u32,
    pub return_quote_buf: [u8; RET_QUOTE_BUF_LEN as usize],
}

const REPORT_BUF_LEN: usize = 2048;
const SIG_BUF_LEN: usize = 2048;
const CERT_BUF_LEN: usize = 2048;

#[repr(C)]
pub struct SGXQuoteVerificationC {
    pub report_buf: [u8; REPORT_BUF_LEN],
    pub report_len: usize,

    pub sig_buf: [u8; SIG_BUF_LEN],
    pub sig_len: usize,

    pub cert_buf: [u8; CERT_BUF_LEN],
    pub cert_len: usize,
}

/// Checks the two conventional outputs of an ecall
///
/// It seems like both outputs should be equivalent but they are not, see SGX programmer's guide for details.
// TODO 2361: Decide on one error handling convention and stick to it, either this or panic.
pub fn ensure_ecall_success(status: SgxStatus, retval: Option<SgxStatus>) -> anyhow::Result<()> {
    ensure!(
        status == SgxStatus::Success,
        "Ecall failed with sgx_status={}",
        status
    );
    if let Some(retval) = retval {
        ensure!(
            retval == SgxStatus::Success,
            "Ecall failed with retval={}",
            retval
        );
    }
    Ok(())
}

pub fn launch_enclave(share_dir: &str) -> Result<SgxEnclave> {
    let enclave_file: PathBuf = Path::new(&share_dir).join("enclave.signed.so");
    ensure!(
        enclave_file.exists(),
        "Enclave file not found {:?}",
        enclave_file
    );
    // only enable debug launch mode in sgx debug mode or prerelease mode
    let sgx_prerelease = std::env::var("SGX_PRERELEASE")
        .map(|v| v.to_lowercase() == "true" || v == "1")
        .unwrap_or(false);
    let sgx_debug = std::env::var("SGX_DEBUG")
        .map(|v| v.to_lowercase() == "true" || v == "1")
        .unwrap_or(false);
    let debug = sgx_debug || sgx_prerelease;
    let enclave = SgxEnclave::create(enclave_file, debug)?;
    Ok(enclave)
}

pub fn init_enclave_diagnostics(id: EnclaveId, pretty_logs: bool) -> Result<()> {
    let status = unsafe { ecall_init_diagnostics(id, pretty_logs) };
    ensure_ecall_success(status, None)?;
    Ok(())
}

/// Initializes the enclave using the sealed data provided
///
/// The sealed data contains essential parameters like the signing key. The enclave must
/// unseal it then store in encrypted memory before being usable. If the sealed data is empty
/// the enclave generates it ad-hoc then returns it sealed. The sealed data returned by this
/// function can be persisted for future init of the same enclave.
pub fn init_enclave(
    enclave: SgxEnclave,
    sealed_data: SealedData,
    custodian_address: CustodianAddress,
    pretty_logs: bool,
) -> Result<(SgxEnclave, SealedData)> {
    init_enclave_diagnostics(enclave.eid(), pretty_logs)?;
    let sealed_data_ser = serde_cbor::to_vec(&sealed_data).unwrap();
    let custodian_address_: [u8; CUSTODIAN_ADDRESS_BYTE_LEN] = custodian_address.into();
    let mut sealed_out: Vec<u8> = vec![0; SEAL_DATA_BUFFER_SIZE];
    let sealed_out_slice = &mut sealed_out[..];
    let mut retval = SgxStatus::Success;
    let mut sealed_out_len: usize = 0;
    let status = unsafe {
        ecall_init_sealed(
            enclave.eid(),
            &mut retval,
            sealed_data_ser.as_ptr(),
            sealed_data_ser.len(),
            &custodian_address_,
            sealed_out_slice.as_mut_ptr(),
            SEAL_DATA_BUFFER_SIZE,
            &mut sealed_out_len as *mut usize,
        )
    };
    ensure_ecall_success(status, Some(retval))?;
    let sealed_data_ser: Vec<u8> = sealed_out_slice[..sealed_out_len].to_vec();
    let sealed_data: SealedData = serde_cbor::from_slice(&sealed_data_ser).unwrap();
    Ok((enclave, sealed_data))
}

pub async fn get_sealed_data(
    txn: &mut Transaction<'_>,
    release_hash: ReleaseHash,
    schema_name: &str,
) -> Result<SealedData> {
    let sql = format!(
        "SELECT discriminant, sealed_log FROM {}.sealed_data WHERE release_hash = $1",
        schema_name
    );
    let mut sealed_data = HashMap::new();
    let rows = txn.query(&sql, &[&release_hash.0.as_bytes()]).await?;
    for row in rows {
        let discriminant: i16 = row.get("discriminant");
        let key = SealedDataKey::try_from(discriminant)?;
        let sealed_log: Vec<u8> = row.get("sealed_log");
        sealed_data.insert(key, sealed_log);
    }
    Ok(SealedData(sealed_data))
}

#[tracing::instrument(level = "info", skip_all, fields(sealed_data_size))]
pub async fn wait_for_sealed_data(
    release_hash: ReleaseHash,
    schema_name: &str,
    pool: &Pool,
) -> Result<SealedData> {
    let mut client = pool.get().await?;
    let mut sealed_data;
    let mut count = 1;
    loop {
        if count % 60 == 0 {
            tracing::error!(?count, "Still waiting for sealed data");
        }
        let mut db_txn = client.transaction().await?;
        sealed_data = get_sealed_data(&mut db_txn, release_hash, schema_name).await?;
        if !sealed_data.0.is_empty() {
            tracing::info!(size=%sealed_data.0.len(), "Sealed data found in db.");
            break;
        }
        tracing::debug!("Sealed data not found in db, retrying in 1s...");
        count += 1;
        sleep(Duration::from_secs(1));
    }
    tracing::Span::current().record("sealed_data_size", sealed_data.0.len());
    Ok(sealed_data)
}

#[tracing::instrument(level = "trace", skip_all)]
pub async fn save_sealed_data(
    txn: &mut Transaction<'_>,
    sealed_data: SealedData,
    release_hash: ReleaseHash,
    schema_name: &str,
) -> Result<()> {
    let sql = format!(
        "
INSERT INTO {}.sealed_data (release_hash, discriminant, sealed_log)
     VALUES ($1, $2, $3)
",
        schema_name
    );
    for (key, sealed_log) in sealed_data.0 {
        let row = txn
            .execute(
                &sql,
                &[&release_hash.0.as_bytes(), &(key as i16), &sealed_log],
            )
            .await?;
        ensure!(row == 1, "Failed to insert sealed data");
    }
    Ok(())
}

pub async fn init_hard_state(
    enclave: SgxEnclave,
    node_id: OperatorNodeId,
    pool: &Pool,
    custodian_address: CustodianAddress,
    schema_name: &str,
    tracing_format: bool,
) -> Result<SgxEnclave> {
    let mut client = pool.get().await?;
    let mut db_txn = client.transaction().await?;
    let release_hash = get_release_mr(enclave.eid())?.release_hash;
    let existing_sealed_data = get_sealed_data(&mut db_txn, release_hash, schema_name).await?;
    let existing_node_id = crate::node::db::get(&db_txn, schema_name, KEY_NODE_ID).await?;
    let enclave = if existing_sealed_data.user_data().is_none() {
        let value = serde_json::to_value(node_id)?;
        crate::node::db::upsert(&db_txn, schema_name, KEY_NODE_ID, &value).await?;
        let (enclave, sealed_data) = init_enclave(
            enclave,
            SealedData::default(),
            custodian_address,
            tracing_format,
        )?;
        save_sealed_data(&mut db_txn, sealed_data, release_hash, schema_name).await?;
        db_txn.commit().await?;
        tracing::info!(
            eid=%enclave.eid(),
            "New enclave successfully initialized",
        );
        enclave
    } else if existing_node_id.is_some() {
        let (enclave, _) = init_enclave(
            enclave,
            existing_sealed_data,
            custodian_address,
            tracing_format,
        )?;
        tracing::info!(
            eid=%enclave.eid(),
            "Existing enclave successfully initialized",
        );
        enclave
    } else {
        bail!("Found sealed data without node_id");
    };
    Ok(enclave)
}

pub fn get_signing_address(eid: EnclaveId) -> Result<Address> {
    let mut fixed_bytes = [0_u8; ADDRESS_BYTE_LEN];
    let status = unsafe { ecall_get_signing_address(eid, &mut fixed_bytes) };
    ensure_ecall_success(status, None)?;
    Ok(Address::from(fixed_bytes))
}

#[tracing::instrument(level = "info", skip_all, fields(mr_signer, release_mr))]
pub fn get_release_mr(eid: EnclaveId) -> Result<ReleaseMeasurement> {
    let target_info = TargetInfo::default();
    let mut report = Report::default();
    let mut retval = SgxStatus::Success;
    let status =
        unsafe { ecall_get_registration_report(eid, &mut retval, &target_info, &mut report) };
    ensure_ecall_success(status, Some(retval))?;
    let sgx_debug = report
        .body
        .attributes
        .flags
        .intersects(AttributesFlags::DEBUG);
    // Check if the both app and enclave have the same build mode
    let sgx_prerelease = std::env::var("SGX_PRERELEASE")
        .map(|v| v.to_lowercase() == "true" || v == "1")
        .unwrap_or(false);
    // We only skip the check in release mode
    if !sgx_prerelease && sgx_debug != cfg!(debug_assertions) {
        // if there is mismatch between enclave and app debug mode,
        // panic since it is a critical error
        tracing::error!(
            "sgx_debug={}, cfg!(debug_assertions)={}",
            sgx_debug,
            cfg!(debug_assertions)
        );
        panic!("Mismatch between enclave and app debug mode");
    }
    let release_mr = ReleaseMeasurement::new(
        report.body.mr_enclave.m.as_slice(),
        report.body.isv_svn,
        sgx_debug,
    );
    tracing::Span::current().record(
        "mr_signer",
        format!(
            "{:?}",
            Bytes32::from_slice(report.body.mr_signer.m.as_slice())
        ),
    );
    tracing::Span::current().record("release_mr", format!("{:?}", release_mr));
    Ok(release_mr)
}

pub fn get_encryption_key(eid: EnclaveId) -> Result<CompressedKey> {
    let mut fixed_bytes = [0_u8; COMPRESSED_KEY_BYTE_LEN];
    let status = unsafe { ecall_get_encryption_key(eid, &mut fixed_bytes) };
    ensure_ecall_success(status, None)?;
    let compressed_key = CompressedKey::from_slice(fixed_bytes.as_slice());
    Ok(compressed_key)
}

#[derive(Debug)]
pub struct QuoteVerification {
    pub report: String,
    pub sig: String,
    pub cert: String,
}

impl QuoteVerification {
    pub fn from_c(verification: SGXQuoteVerificationC) -> Result<Self> {
        let result = Self {
            report: str::from_utf8(&verification.report_buf[..verification.report_len])?
                .to_string(),
            sig: str::from_utf8(&verification.sig_buf[..verification.sig_len])?.to_string(),
            cert: str::from_utf8(&verification.cert_buf[..verification.cert_len])?.to_string(),
        };
        Ok(result)
    }

    // Convert the report to hex string
    pub fn hex_coded_report(&self) -> String {
        format!(
            "0x{}",
            self.report
                .as_bytes()
                .iter()
                .map(|b| format!("{:02x?}", b))
                .collect::<Vec<String>>()
                .join("")
        )
    }

    // Decode the base64 encoded signature
    pub fn decode_sig(&self) -> Result<Vec<u8>> {
        Ok(base64_url::decode(&self.sig)?)
    }

    // Convert the base64 encoded signature to hex string
    pub fn hex_coded_sig(&self) -> Result<String> {
        let decoded = self.decode_sig()?;
        Ok(format!(
            "0x{}",
            decoded
                .iter()
                .map(|b| format!("{:02x?}", b))
                .collect::<Vec<String>>()
                .join("")
        ))
    }
}

#[cfg(not(feature = "sw"))]
pub fn make_quote(eid: EnclaveId) -> Result<SGXQuoteC> {
    use sgx_types::{
        error::Quote3Error,
        function::{sgx_qe_get_quote, sgx_qe_get_quote_size, sgx_qe_get_target_info},
    };

    let mut ti: TargetInfo = TargetInfo::default();
    tracing::debug!("Step1: Call sgx_qe_get_target_info:");
    let qe3_ret = unsafe { sgx_qe_get_target_info(&mut ti as *mut _) };
    ensure!(
        qe3_ret == Quote3Error::Success,
        "Quote Enclave failed with error={:?}",
        qe3_ret
    );

    tracing::debug!("Succeed!\nStep2: Call create_app_report:");
    let mut retval = SgxStatus::default();
    let mut report = Report::default();
    let status = unsafe { ecall_get_registration_report(eid, &mut retval, &ti, &mut report) };
    ensure_ecall_success(status, Some(retval))?;

    let mut quote_size: u32 = 0;
    let qe3_ret = unsafe { sgx_qe_get_quote_size(&mut quote_size) };
    ensure!(
        qe3_ret == Quote3Error::Success,
        "Error in sgx_qe_get_quote_size: {:?}",
        qe3_ret
    );
    ensure!(
        quote_size < RET_QUOTE_BUF_LEN,
        "Quote size {} overflow the buffer",
        quote_size
    );
    tracing::debug!("Succeed!\nStep4: Call sgx_qe_get_quote:");
    let mut return_quote_buf = [0u8; RET_QUOTE_BUF_LEN as usize];
    let qe3_ret = unsafe { sgx_qe_get_quote(&report, quote_size, return_quote_buf.as_mut_ptr()) };
    ensure!(
        qe3_ret == Quote3Error::Success,
        "Error in sgx_qe_get_quote: {:?}",
        qe3_ret
    );

    tracing::debug!("succeed!");

    Ok(SGXQuoteC {
        qe_report: report,
        ti,
        quote_nonce: QuoteNonce::default(),
        quote_len: quote_size,
        return_quote_buf,
    })
}

// In the software simulation mode, we generate a dummy quote with a self-report
// This report cannot pass the cryptographic verification but only for dev & test purposes.
#[cfg(feature = "sw")]
pub fn make_quote(eid: EnclaveId) -> Result<SGXQuoteC> {
    let ti: TargetInfo = TargetInfo::default();
    let mut retval = SgxStatus::default();
    let mut report = Report::default();
    let status = unsafe { ecall_get_registration_report(eid, &mut retval, &ti, &mut report) };
    ensure_ecall_success(status, Some(retval))?;
    let return_quote_buf = [0u8; RET_QUOTE_BUF_LEN as usize];
    Ok(SGXQuoteC {
        qe_report: report,
        ti,
        quote_nonce: QuoteNonce::default(),
        quote_len: RET_QUOTE_BUF_LEN,
        return_quote_buf,
    })
}

// Verify DCAP quote.
// To get Intel-signed quote, the DCAP feature/mode must use the API KEY from Intel as a paid service (capped 10000 API call per year).
pub async fn verify_quote(eid: EnclaveId, quote: &SGXQuoteC) -> Result<QuoteVerification> {
    let mut runtime_data = [0u8; 40];
    let status = unsafe { ecall_get_user_data(eid, &mut runtime_data) };
    ensure_ecall_success(status, None)?;
    // Get signing cert from azure attestation
    // NOTE: Using this creates a tokio runtime, so this function should not be called from an async context.
    let client = reqwest::Client::new();
    let res = client.get(ATTESTATION_CERT_URL).send().await?;
    let resp_text = res.text().await?;
    // println!("{resp_text}");
    let raw_key_set: RawJsonWebKeySet = serde_json::from_str(&resp_text)?;
    let jwk_set: JsonWebKeySet = raw_key_set.try_into()?;
    // strip the PEM cert
    let pem = jwk_set.keys[0].key.try_to_pem()?;
    let v: Vec<&str> = pem.split("-----").collect();
    let cert = v[2].to_string().replace('\n', "");
    let report_type = std::env::var("REPORT_TYPE").expect("REPORT_TYPE is not set");
    let verification = if cfg!(feature = "self_ra") {
        ensure!(
            report_type == "SELF",
            "REPORT_TYPE is not set to SELF, but to {}",
            report_type
        );
        // Generate clams from the report and packed with test header and signature
        let header = Header::self_signed();
        let mrenclave = quote.qe_report.body.mr_enclave.m.to_hex();
        let mrsigner = quote.qe_report.body.mr_signer.m.to_hex();
        // report embedded data
        let mut report_data = [0u8; 64];
        let mut hasher = Sha256::new();
        hasher.update(runtime_data);
        report_data[..32].copy_from_slice(&hasher.finalize());
        let claims = TokenClaims {
            x_ms_sgx_ehd: base64::engine::general_purpose::STANDARD.encode(runtime_data),
            x_ms_sgx_is_debuggable: quote
                .qe_report
                .body
                .attributes
                .flags
                .intersects(AttributesFlags::DEBUG),
            x_ms_sgx_mrenclave: mrenclave,
            x_ms_sgx_mrsigner: mrsigner,
            x_ms_sgx_svn: quote.qe_report.body.isv_svn,
            x_ms_sgx_report_data: report_data.to_hex(),
        };
        let json_header = serde_json::to_string(&header)?;
        let json_body = serde_json::to_string(&claims)?;
        QuoteVerification {
            report: base64_url::encode(&json_header)
                + "."
                + base64_url::encode(&json_body).as_str(),
            sig: TEST_SIGNATURE.to_string(),
            cert,
        }
    } else {
        // Note:
        // Only request Intel signed report with the DCAP feature, which means
        // the DCAP feature/mode must use the API KEY from Intel as a paid service (capped 10000 API call per year).
        // compare the env var REPORT_TYPE to "DCAP" to ensure the correct report type
        ensure!(
            report_type == "DCAP",
            "REPORT_TYPE is not set to DCAP, but to {}",
            report_type
        );
        // The self_ra feature shall be only disabled with the release build in production environments.
        assert!(!cfg!(debug_assertions));
        let quote_data = quote.return_quote_buf[..quote.quote_len as usize].to_vec();
        let attest_request = AzureSgxAttestationRequest::from_bytes(&quote_data, &runtime_data);
        // request for azure attestation
        let res = client
            .post(format!(
                "{}{}",
                ATTESTATION_PROVIDER_URL, SGX_ATTESTATION_URI
            ))
            .header("Accept", "application/json")
            .header(
                "X-API-KEY",
                std::env::var("ITA_API_KEY").expect("ITA_API_KEY is not set"),
            )
            .header("Content-Type", "application/json")
            .json(&attest_request)
            .send()
            .await?;
        let jwt = res.json::<JwtResponse>().await?.token;
        // println!("{:?}", jwt);
        // Verify azure signature
        let claims = validate_json_web_token(jwt.clone(), jwk_set)?;
        // Verify claims
        tracing::debug!(
            "Verified SGX debuggable status: {}",
            claims.x_ms_sgx_is_debuggable
        );
        tracing::debug!(
            "Verified SGX enclave measurement: {}",
            claims.x_ms_sgx_mrenclave
        );
        tracing::debug!(
            "Verified SGX signer measurement: {}",
            claims.x_ms_sgx_mrsigner
        );
        tracing::debug!("Verified SGX SGX SVN: {}", claims.x_ms_sgx_svn);
        tracing::debug!(
            "Verified SGX runtime data: {}",
            base64::engine::general_purpose::STANDARD
                .decode(&claims.x_ms_sgx_ehd)
                .unwrap()
                .to_hex::<String>(),
        );
        // split jwt into pieces
        let parts: Vec<&str> = jwt.rsplitn(2, '.').collect();
        QuoteVerification {
            report: parts[1].to_string(),
            sig: parts[0].to_string(),
            cert,
        }
    };
    Ok(verification)
}
