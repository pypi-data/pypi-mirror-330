use anyhow::Result;
use base64::Engine;
use jsonwebkey::{JsonWebKey, Key, PublicExponent, RsaPublic};
use jsonwebtoken as jwt;
use serde::{Deserialize, Serialize};
use std::convert::TryFrom;
use x509_certificate::{X509Certificate, X509CertificateError};

pub(crate) const ATTESTATION_PROVIDER_URL: &str = "https://api.trustauthority.intel.com";
pub(crate) const ATTESTATION_CERT_URL: &str = "https://portal.trustauthority.intel.com/certs";
pub(crate) const SGX_ATTESTATION_URI: &str = "/azure-attestation/attest/SgxEnclave";
pub(crate) const TEST_SIGNATURE: &str = "t0Kc9YOD5OELas5bC-LJJql8EzAA8dWPs0k-L-688ScwiCQw5NbVntonB3VPRRQbUqAY3Y1-peREnW3jjMBgPMi0uLkAoPzOFhEDqphrNZmnH9AIMUICUVInaMF5HgudzGSlr5VmzR-JRMukq7DsCr6pbZYbkJLlxj1okMNrbiKKokzMkhFJvPLRTPdngW3XVqQ_4hDpg32ovwMScAE8C4TPCFkvZOlSj26VHSZti6GJhrtAXOaMsCTiOZJ8liY9HwCDdQkpMISRI4VVisO51tdqXaEMn6z4-f7FoVA_9xcjqBgNaJr31e32SfMn0S0QpeDtZhVCXyylzHU2-dbom6C2nnRjiheZXj1saFhSQg_vH74_mU28_6t1VF8lXTFaKHGf2U4m8fc1oJVY6JHDGvIstboxh52czrVbEBsaFJ_iFGfsitmcm4GgGM6vpoPZo5MV5QPvT-fOvTyux86MqJzb6Zx-GbKjktGkOSIjQwS5d_1-ogsspSkuXojvFWQM";
const TEST_KEY_ID: &str = "79d80711b754cceb307d4278dc59957f27eb55a8e33d3b824967975843dcbf21df924eebaf93fce186fd291d36817785";

#[derive(Serialize)]
pub struct RegistrationData {
    pub report: String,
    pub signature: String,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub(crate) struct AzureSgxAttestationRequest {
    quote: String,
    runtime_data: SgxRuntimeData,
}

impl AzureSgxAttestationRequest {
    pub fn from_bytes(quote_data: &[u8], runtime_data: &[u8]) -> Self {
        Self {
            quote: base64_url::encode(quote_data),
            runtime_data: SgxRuntimeData::new_binary(runtime_data),
        }
    }
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct SgxRuntimeData {
    data: String,
    data_type: String,
}

impl SgxRuntimeData {
    fn new_binary(data: &[u8]) -> Self {
        Self {
            data: base64::engine::general_purpose::STANDARD.encode(data),
            data_type: "Binary".to_string(),
        }
    }
}

#[derive(Deserialize)]
pub(crate) struct JwtResponse {
    pub token: String,
}
#[derive(Deserialize)]
pub(crate) struct RawJsonWebKey {
    pub x5c: Vec<String>,
    pub kid: String,
    pub kty: String,
    pub alg: String,
}
#[derive(Deserialize)]
pub(crate) struct RawJsonWebKeySet {
    pub keys: Vec<RawJsonWebKey>,
}

#[derive(Debug)]
pub(crate) struct JsonWebKeySet {
    pub keys: Vec<JsonWebKey>,
}

impl TryFrom<RawJsonWebKeySet> for JsonWebKeySet {
    type Error = X509CertificateError;
    // This method only works for RS256 algorithm using by Azure Attestation Adapter
    fn try_from(raw_set: RawJsonWebKeySet) -> Result<Self, X509CertificateError> {
        let mut keys = Vec::new();
        for key in raw_set.keys {
            if key.alg == "RS256" && key.kty == "RSA" {
                let raw_cert = base64::engine::general_purpose::STANDARD
                    .decode(key.x5c[0].clone())
                    .unwrap();
                let x509 = X509Certificate::from_der(raw_cert)?;
                let pubkey = x509.rsa_public_key_data()?;
                let rsa_pub = RsaPublic {
                    e: PublicExponent,
                    n: pubkey.modulus.as_slice().into(),
                };
                let rsa_key = Key::RSA {
                    public: rsa_pub,
                    private: None,
                };
                let mut jwk = JsonWebKey::new(rsa_key);
                jwk.key_id = Some(key.kid);
                keys.push(jwk);
                return Ok(JsonWebKeySet { keys });
            }
        }
        Err(X509CertificateError::Other(
            "Cannot find RSA key".to_string(),
        ))
    }
}
#[derive(Debug, Deserialize, Serialize)]
#[serde(rename_all = "kebab-case")]
pub struct TokenClaims {
    pub x_ms_sgx_ehd: String,
    pub x_ms_sgx_is_debuggable: bool,
    pub x_ms_sgx_mrenclave: String,
    pub x_ms_sgx_mrsigner: String,
    // pub x_ms_sgx_product_id: u16,
    pub x_ms_sgx_report_data: String,
    pub x_ms_sgx_svn: u16,
}

#[derive(Debug, Deserialize, Serialize)]
pub(crate) struct Header {
    pub alg: String,
    pub jku: String,
    pub kid: String,
    pub typ: String,
}

impl Header {
    pub fn self_signed() -> Self {
        Self {
            alg: "RS256".to_string(),
            jku: ATTESTATION_PROVIDER_URL.to_string(),
            kid: TEST_KEY_ID.to_string(),
            typ: "JWT".to_string(),
        }
    }
}
/// Validate JsonWebToken with JsonWebKeySet,
/// only works for RS256 algorithm and token from default attestation provider.
pub(crate) fn validate_json_web_token(
    jwt: String,
    jwks: JsonWebKeySet,
) -> jwt::errors::Result<TokenClaims> {
    let header = jwt::decode_header(&jwt)?;
    if header.kid.is_none() {
        return Err(jwt::errors::Error::from(
            jwt::errors::ErrorKind::InvalidToken,
        ));
    }
    // find the corresponding key
    let mut idx: Option<usize> = None;
    for (i, key) in jwks.keys.iter().enumerate() {
        if key.key_id.is_some() && key.key_id == header.kid {
            idx = Some(i);
        }
    }
    if idx.is_none() {
        // cannot find corresponding pubkey
        return Err(jwt::errors::Error::from(
            jwt::errors::ErrorKind::InvalidRsaKey(header.kid.unwrap()),
        ));
    }
    let pem = jwks.keys[idx.unwrap()].key.try_to_pem().unwrap();
    // println!("\n{pem}");
    let key = jwt::DecodingKey::from_rsa_pem(pem.as_bytes())?;
    // prepare validation
    let algo = jwt::Algorithm::RS256;
    let mut validation = jwt::Validation::new(algo);
    validation.validate_exp = false;
    // decode JWT with the public key
    Ok(jwt::decode::<TokenClaims>(&jwt, &key, &validation)?.claims)
}

#[cfg(test)]
mod tests {
    use super::*;
    use rustc_hex::ToHex;

    const RAW_KEY_SET: &str = r#"{
            "keys": [
              {
                "alg": "RS256",
                "e": "AQAB",
                "kid": "79d80711b754cceb307d4278dc59957f27eb55a8e33d3b824967975843dcbf21df924eebaf93fce186fd291d36817785",
                "kty": "RSA",
                "n": "yE07D7FRSXLsswdeK7h22kw-Xv2K2r4NFoefWElZ6FWmLvCcd27wGEczNeKrE91SWczPtR279tTasQN6_v8qsswC5rCGYlrRWvE0vuPoUXezlV4PX0tCJJJmxWtXFXW0dChWvR1j-_viOItfR8jrybV2-DyVBgGX1ad4BLJJseglPXcofhnKYcG9gp8J2zPFqs1tu6jTW-He3Xw7ZeQNq0n4ZfrRBM3GEYVVsWGlTlqVidMhbvMXSQgz1x2QjyPC2mSUrT-JyA2xTm84Mv_Lmz6FpHXsjXMyPKCUVUf8LSTAiw3UsHa-7QGUW51hh9lZsbWkdSfwGUGxjrcMNEwYo3KvcF8f9Cv1_bkla396poQhtTIHuV478PobzsCfdkbCF5CfwZN31KbqyD9o9pVyzmmQUmOikIZuiSPRnfIU_P8duM5F6yvxQPITZf1RhOPBNYLiOJge7C89OmsM46UKtAYNTieBH-J8oWUUWfAX3pO38bKIzNwHDelSbaeHterJ",
                "x5c": [
                  "MIIE/DCCA2SgAwIBAgIBATANBgkqhkiG9w0BAQ0FADBlMQswCQYDVQQGEwJVUzELMAkGA1UECAwCQ0ExGjAYBgNVBAoMEUludGVsIENvcnBvcmF0aW9uMS0wKwYDVQQDDCRJbnRlbCBUcnVzdCBBdXRob3JpdHkgQVRTIFNpZ25pbmcgQ0EwHhcNMjMwOTEyMTExMTUxWhcNMjQwOTExMTExMTUxWjBwMQswCQYDVQQGEwJVUzELMAkGA1UECAwCQ0ExGjAYBgNVBAoMEUludGVsIENvcnBvcmF0aW9uMTgwNgYDVQQDDC9JbnRlbCBUcnVzdCBBdXRob3JpdHkgQXR0ZXN0YXRpb24gVG9rZW4gU2lnbmluZzCCAaIwDQYJKoZIhvcNAQEBBQADggGPADCCAYoCggGBAMhNOw+xUUly7LMHXiu4dtpMPl79itq+DRaHn1hJWehVpi7wnHdu8BhHMzXiqxPdUlnMz7Udu/bU2rEDev7/KrLMAuawhmJa0VrxNL7j6FF3s5VeD19LQiSSZsVrVxV1tHQoVr0dY/v74jiLX0fI68m1dvg8lQYBl9WneASySbHoJT13KH4ZymHBvYKfCdszxarNbbuo01vh3t18O2XkDatJ+GX60QTNxhGFVbFhpU5alYnTIW7zF0kIM9cdkI8jwtpklK0/icgNsU5vODL/y5s+haR17I1zMjyglFVH/C0kwIsN1LB2vu0BlFudYYfZWbG1pHUn8BlBsY63DDRMGKNyr3BfH/Qr9f25JWt/eqaEIbUyB7leO/D6G87An3ZGwheQn8GTd9Sm6sg/aPaVcs5pkFJjopCGbokj0Z3yFPz/HbjOResr8UDyE2X9UYTjwTWC4jiYHuwvPTprDOOlCrQGDU4ngR/ifKFlFFnwF96Tt/GyiMzcBw3pUm2nh7XqyQIDAQABo4GrMIGoMAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFGXRi1GAPlb8fBXUcGQrN5P0nrQAMB8GA1UdIwQYMBaAFCRX9lEHLr6HXZtQaFKogfoiHFl5MAsGA1UdDwQEAwIE8DBLBgNVHR8ERDBCMECgPqA8hjpodHRwczovL3BvcnRhbC50cnVzdGF1dGhvcml0eS5pbnRlbC5jb20vY3JsL2F0cy1jYS1jcmwuZGVyMA0GCSqGSIb3DQEBDQUAA4IBgQCHwDA/kgYi1qZNb7GpO3HpwLP+sjRW2Jm79kgAFORLloW8lPPJab4yl52rNdk2PKl6qsDNwaHrcR4jfe0mxyrdCO2nMtSxJziYK9unwAPF8aCuB4Nym5VNxoVkTvI1r+KMIfBi8eWAREPoH6DgC9bUrqIyXh0zfxTBy3d9rL9+N6OXmP4z6JmzF54ZJnrJJgfKdZ5ClanwDalcLDZSPMTIEZRaagN6PGEUVawCsg+klBBCfgt2j2+Ta3Ri/kCATOmxfRrJSCXYzD2mrcvxHrXIyPT2sRYSNR9nXSwoEH9okfabs0duItQ1fZmKG5j0qAxtQ1vONANpKSIjXSnam89KfaG/xr3x6Z5uq+y7XPSg5gnzn5rLaafuPcSFYthpoX3kYTIUMuO/sqt42x2Ka1sndaAlCEPHfIBys1yBgda0tl+O6d1HVwJ79DBEXqLQftAueGvQSHsIbExkiJvw7Mhdvcid6sb2z8GOY4Ljqj0LHmMi6c1JoyKrkKK9167rW4c=",
                  "MIIFCjCCA3KgAwIBAgIBATANBgkqhkiG9w0BAQ0FADB0MSYwJAYDVQQDDB1JbnRlbCBUcnVzdCBBdXRob3JpdHkgUm9vdCBDQTELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAkNBMRQwEgYDVQQHDAtTYW50YSBDbGFyYTEaMBgGA1UECgwRSW50ZWwgQ29ycG9yYXRpb24wHhcNMjMwOTEyMTExMTQ5WhcNMzYxMjMwMTExMTQ5WjBlMQswCQYDVQQGEwJVUzELMAkGA1UECAwCQ0ExGjAYBgNVBAoMEUludGVsIENvcnBvcmF0aW9uMS0wKwYDVQQDDCRJbnRlbCBUcnVzdCBBdXRob3JpdHkgQVRTIFNpZ25pbmcgQ0EwggGiMA0GCSqGSIb3DQEBAQUAA4IBjwAwggGKAoIBgQCof1PJ6PFnZ5TOyxBP8H7kyBxsAopUcMZtJAIdLZV+L+5DVMvH6E/hT4+7XX5SGYkb0R+XquyBz0PayzVrs71k8nL0MrwBIKLuIWQEcmTLC5/18Njf7QxBDZ3+uFrTOcfYcfYpfTNl2v/RvjEM6+KuDhxqLlH//buRO9eALngQQDqHq7pigrB9vVoOtpdng5Az4kjlDOOmdrNNigpEP4u4sQsqcAkSUFbofTXk8OiWtWClL6ItjosedwcabcdXSkAhf/T0QfYCcRQBOhSIblveZbaWgVXKb4S+HlM1Ft/QEtHNpuldlyI/s7+0ISAzVM8vRZU27EuPpQBUseNIrH2+DXTtpop13tozOl64o7VJmB7mwi+Zqv31NT0BucvMUdeC/bg2RSIKlV6RRomUTKtMFo3RpBi3K7+GUMbiq5GNQBNece294wHDhtgA+Bjg59IIxsHx3O9PmTgGAxmx8qAN2e9FPObTNWIHijfue6D0RkbolJd1/BGgAFcmF3pZy+cCAwEAAaOBtTCBsjASBgNVHRMBAf8ECDAGAQH/AgEAMB0GA1UdDgQWBBQkV/ZRBy6+h12bUGhSqIH6IhxZeTAfBgNVHSMEGDAWgBTzCwdViUpG9BjW2nyu+DI+d6gWETAOBgNVHQ8BAf8EBAMCAQYwTAYDVR0fBEUwQzBBoD+gPYY7aHR0cHM6Ly9wb3J0YWwudHJ1c3RhdXRob3JpdHkuaW50ZWwuY29tL2NybC9yb290LWNhLWNybC5kZXIwDQYJKoZIhvcNAQENBQADggGBADtWnJTjnCT6P5GZHS7Qz6MsrpM2IBwWcpnayTe+nV0CAqk4RJay7rupzq8gn8PllPXyWFoComrsT6HPZ80uh0JUIACOmNcO5UhwuRxML+EPmgpVVQJlz68AXf99Y1HaJxJ0aHkFSPr11XUOQ3S657QKee7RJijwcYu6rgfw6eVnYCGr7UD6SSW63D9nZLsa11v8GcIDWPdZVkyPnDVNJulAuWby/FQtZWAs4vCmxWpJYWoy303AVRzEBYoiyBRznWbed0ykyVU6TogLuezoxwH6jrZ7NeaFKrpbnD1YvI3JfP6EzPo1EqjpfumlVW99yY80mrHdr7FpIe9h9RL05utnYcoGt2VzbwN0H3ZXFPBwsBoioLX17xtSM7894w/rHdQV9wEMvxUT2Hmo+rRNu6lCQ3gDsLVXPvBd5rB3tnEY7wYu/uaLvHf01lq9/X9aTuISg63pFsqcb9oCS3hnx//b47/oHjo7yYCPhgKWHJdC5yiiv6U2NqQLeM9FtZIPuQ==",
                  "MIIE2TCCA0GgAwIBAgIUZZX2XASGiYPzpZfwGNa7QFlK+3QwDQYJKoZIhvcNAQENBQAwdDEmMCQGA1UEAwwdSW50ZWwgVHJ1c3QgQXV0aG9yaXR5IFJvb3QgQ0ExCzAJBgNVBAYTAlVTMQswCQYDVQQIDAJDQTEUMBIGA1UEBwwLU2FudGEgQ2xhcmExGjAYBgNVBAoMEUludGVsIENvcnBvcmF0aW9uMB4XDTIzMDkxMjExMTE0OFoXDTQ5MTIzMDExMTE0OFowdDEmMCQGA1UEAwwdSW50ZWwgVHJ1c3QgQXV0aG9yaXR5IFJvb3QgQ0ExCzAJBgNVBAYTAlVTMQswCQYDVQQIDAJDQTEUMBIGA1UEBwwLU2FudGEgQ2xhcmExGjAYBgNVBAoMEUludGVsIENvcnBvcmF0aW9uMIIBojANBgkqhkiG9w0BAQEFAAOCAY8AMIIBigKCAYEAuQ1g1Q4MtnvTRhYITKVou5CDvB5FpfjBe8ssUKaDILwkgJlGNv66IWPQ9vhIekZQjuvHbUj9yPcrM7Hva7h7Ehlo/Sm7ZhY8AgZfGFTRJjvNU+vg/BTr5vuqUu/a54eewyzMcmxwmWhK/4cGQs7spFB346jpjSgOHgk5PgJ39PgEr5UL9SvJ1LFRuCNxZTdzyLe7K8cWvEnwGkR2RJpK9pYgzfnAWy8J0djdAKaoQxt8TOE/IwafG/0ujTeuNbzo+3wxeF6SGz56MimE1+KgraPpULaeX2tAL9lUz+ECMetNLbAyqHQwxN1jQZ/3VgpQ8qqh7Cyo4rEjpja29iRtOihBYlW0/X6TxOG1LLSuGo/N9CcSW6EzjsC1Bzakzjs4OD+JGaqqvc255p8URTxZSRSJr1xtimZK+BJoCHECsrCLvCC5UmFfTQrxkeGJ+OIDMkQFgidUw2K7kYXe9k7glKw9yyVf9C0hhqBFfPD8r+CXEA9m2u1tvR4NGMuoegMxAgMBAAGjYzBhMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFPMLB1WJSkb0GNbafK74Mj53qBYRMB8GA1UdIwQYMBaAFPMLB1WJSkb0GNbafK74Mj53qBYRMA4GA1UdDwEB/wQEAwIBBjANBgkqhkiG9w0BAQ0FAAOCAYEALTVDjOJL3XVuK25K6v/hd4z5vZOzhHK6ifnCjLWKu+CkPbKQMMMYMbYTpqm6gEcSr28dPMOF1IWG4xcJX9oJ6b3mDWj3NQNBomBI8fq0hRgz9hKF8wpFpU3UzXtyBLLL18BTCQeJecb6pwrpASVZNmR/fAv8fbR9wWdTBVFHmIrg1wvU1u2WqYSdAgQGke+WdWFIvZCKKMVAB0jX2kPHBQnAkLF3pRaVyNT4I2MCRB8cW2fbSCIARBeryiIHyGCKnDGkDK+dvPxMJ9eMidPbBQBp5t6jxoicg9X8Gw9MeOboOEOB1sIAd0S25V9fzIwwn6j61K4d2VkLf4ZnDa2VKTgmv6NFMynu+JlHVYhQ0yin+dfD63XJvBLcfLrJwK10lsVMX7xv3dB4P+DBYHtWPwrjE28j6+IjCIupuarzDcahBTbRZIAAW4eWKrA3MPQVyGikcdnciFN7kL12EtHhrSBL2jTzsScWvatPqqzIeNxDCywNEyjtGYLnLBnZnbSP"
                ]
              }
            ]
        }
        "#;

    // The sample JWT from Intel Trust Authority's Azure Attestation Adapter.
    // Format: ${header}.${body}.${signature}
    const RAW_TOKEN: &str = "eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vcG9ydGFsLnRydXN0YXV0aG9yaXR5LmludGVsLmNvbS9jZXJ0cyIsImtpZCI6Ijc5ZDgwNzExYjc1NGNjZWIzMDdkNDI3OGRjNTk5NTdmMjdlYjU1YThlMzNkM2I4MjQ5Njc5NzU4NDNkY2JmMjFkZjkyNGVlYmFmOTNmY2UxODZmZDI5MWQzNjgxNzc4NSIsInR5cCI6IkpXVCJ9\
    .eyJhYXMtZWhkIjoiV21tb2ZXblF5blUzUjNjZ0RlY0lWTEJzWG8xVUNlMENIWktadjJnVUo1cHFGQkduNkdhbU1RPT0iLCJhdHRlc3Rlcl9hZHZpc29yeV9pZHMiOlsiSU5URUwtU0EtMDA4MjgiLCJJTlRFTC1TQS0wMDgzNyIsIklOVEVMLVNBLTAwNjU3IiwiSU5URUwtU0EtMDA3NjciLCJJTlRFTC1TQS0wMDYxNSJdLCJhdHRlc3Rlcl9oZWxkX2RhdGEiOiJXbW1vZlduUXluVTNSM2NnRGVjSVZMQnNYbzFVQ2UwQ0haS1p2MmdVSjVwcUZCR242R2FtTVE9PSIsImF0dGVzdGVyX3RjYl9kYXRlIjoiMjAyMy0wMi0xNVQwMDowMDowMFoiLCJhdHRlc3Rlcl90Y2Jfc3RhdHVzIjoiT3V0T2ZEYXRlQ29uZmlndXJhdGlvbk5lZWRlZCIsImF0dGVzdGVyX3R5cGUiOiJTR1giLCJkYmdzdGF0IjoiZW5hYmxlZCIsImVhdF9wcm9maWxlIjoiaHR0cHM6Ly9wb3J0YWwudHJ1c3RhdXRob3JpdHkuaW50ZWwuY29tL2VhdF9wcm9maWxlLmh0bWwiLCJpbnR1c2UiOiJnZW5lcmljIiwibWFhLWVoZCI6IldtbW9mV25ReW5VM1IzY2dEZWNJVkxCc1hvMVVDZTBDSFpLWnYyZ1VKNXBxRkJHbjZHYW1NUT09IiwicHJvZHVjdC1pZCI6Miwic2d4LW1yZW5jbGF2ZSI6ImUxNmUzODE4OGU0YjBiMDA2OTg0ZTY0M2QyMzM0MTk1MjY1ODQ2OGMwYzZhN2MyMzM3MzFiMWU1MTEyMzhmMzAiLCJzZ3gtbXJzaWduZXIiOiI4M2Q3MTllNzdkZWFjYTE0NzBmNmJhZjYyYTRkNzc0MzAzYzg5OWRiNjkwMjBmOWM3MGVlMWRmYzA4YzdjZTllIiwic2d4X2NvbGxhdGVyYWwiOnsicWVpZGNlcnRoYXNoIjoiYjJjYTcxYjhlODQ5ZDVlNzk5NDUxYjRiZmU0MzE1OWEwZWU1NDgwMzJjZWNiMmMwZTQ3OWJmNmVlM2YzOWZkMSIsInFlaWRjcmxoYXNoIjoiY2E2ODVmZjFmYTU3MmI1ZmQ1YjBkMTBjMWUwNmZjZTQwZjI1NTQ0NzI5YjYwNTI2ODk1ODNhYTE3MTY2YWI4NSIsInFlaWRoYXNoIjoiNDgzYjQ0ZmFlNGI0OTdiZjc3MTFkODEzNWJlMzAzNjMwOGIxMzliYWJkNGE5MjkwMjdhZjUxZTlkM2U5YjYxZSIsInF1b3RlaGFzaCI6IjhmYTQ2YWRjN2I3ZTY5ZjZiZWZkZDE1NGYyODg1NTdkMzlkYTYxNDgxYWU0Yzc4NmY3Y2U0MTM1ZDA2MGJlOTMiLCJ0Y2JpbmZvY2VydGhhc2giOiJiMmNhNzFiOGU4NDlkNWU3OTk0NTFiNGJmZTQzMTU5YTBlZTU0ODAzMmNlY2IyYzBlNDc5YmY2ZWUzZjM5ZmQxIiwidGNiaW5mb2NybGhhc2giOiJjYTY4NWZmMWZhNTcyYjVmZDViMGQxMGMxZTA2ZmNlNDBmMjU1NDQ3MjliNjA1MjY4OTU4M2FhMTcxNjZhYjg1IiwidGNiaW5mb2hhc2giOiI1YWI5NTJmYTI4MzAyZmM1Zjg2M2QzYmNmMGVkNDc0ZjhmMTE3NWZhZDc2MTk0OTFlMmE5ZTkwNzhlMzgyMjI2In0sInNneF9pc19kZWJ1Z2dhYmxlIjp0cnVlLCJzZ3hfaXN2cHJvZGlkIjoyLCJzZ3hfaXN2c3ZuIjowLCJzZ3hfbXJlbmNsYXZlIjoiZTE2ZTM4MTg4ZTRiMGIwMDY5ODRlNjQzZDIzMzQxOTUyNjU4NDY4YzBjNmE3YzIzMzczMWIxZTUxMTIzOGYzMCIsInNneF9tcnNpZ25lciI6IjgzZDcxOWU3N2RlYWNhMTQ3MGY2YmFmNjJhNGQ3NzQzMDNjODk5ZGI2OTAyMGY5YzcwZWUxZGZjMDhjN2NlOWUiLCJzZ3hfcmVwb3J0X2RhdGEiOiI5ZTZjY2Q5M2NiMjAwYjk5NzczYzYwMmI0NzM0NGIzMDg4ZTkzNTVlMDA4YzM4YzIxMTAxN2U0YzRjNDY3NWJkMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMCIsInN2biI6MCwidmVyIjoiMS4wLjAiLCJ2ZXJpZmllcl9pbnN0YW5jZV9pZHMiOlsiMzdjMjQxMmQtOWJhMi00OWNiLWE1NmItZDUzNThmN2JlMDMwIiwiNThiYWVhZjctNWRiMi00MTQ2LWI4M2QtY2YxMDVjZDM5Mjk3IiwiYzkxNDhkMzEtNmIyYy00NzM2LWI2MzMtZmVhZDc3ZDc4MzI2IiwiNzhkZGQzN2UtMTA3ZC00ZDRiLTkwY2UtZTY2N2JjODU1NTM3IiwiMDk5ZDE1YmItNzdjZS00MzdhLWFmNTEtMDlmOWVkZWQ5Y2QzIiwiMmU4ZjI3NDQtZjQ4Yi00ZGNkLTgzNDEtOTBhY2ZlYmFlY2M5Il0sIngtbXMtYXR0ZXN0YXRpb24tdHlwZSI6IlNHWCIsIngtbXMtc2d4LWNvbGxhdGVyYWwiOnsicWVpZGNlcnRoYXNoIjoiYjJjYTcxYjhlODQ5ZDVlNzk5NDUxYjRiZmU0MzE1OWEwZWU1NDgwMzJjZWNiMmMwZTQ3OWJmNmVlM2YzOWZkMSIsInFlaWRjcmxoYXNoIjoiY2E2ODVmZjFmYTU3MmI1ZmQ1YjBkMTBjMWUwNmZjZTQwZjI1NTQ0NzI5YjYwNTI2ODk1ODNhYTE3MTY2YWI4NSIsInFlaWRoYXNoIjoiNDgzYjQ0ZmFlNGI0OTdiZjc3MTFkODEzNWJlMzAzNjMwOGIxMzliYWJkNGE5MjkwMjdhZjUxZTlkM2U5YjYxZSIsInF1b3RlaGFzaCI6IjhmYTQ2YWRjN2I3ZTY5ZjZiZWZkZDE1NGYyODg1NTdkMzlkYTYxNDgxYWU0Yzc4NmY3Y2U0MTM1ZDA2MGJlOTMiLCJ0Y2JpbmZvY2VydGhhc2giOiJiMmNhNzFiOGU4NDlkNWU3OTk0NTFiNGJmZTQzMTU5YTBlZTU0ODAzMmNlY2IyYzBlNDc5YmY2ZWUzZjM5ZmQxIiwidGNiaW5mb2NybGhhc2giOiJjYTY4NWZmMWZhNTcyYjVmZDViMGQxMGMxZTA2ZmNlNDBmMjU1NDQ3MjliNjA1MjY4OTU4M2FhMTcxNjZhYjg1IiwidGNiaW5mb2hhc2giOiI1YWI5NTJmYTI4MzAyZmM1Zjg2M2QzYmNmMGVkNDc0ZjhmMTE3NWZhZDc2MTk0OTFlMmE5ZTkwNzhlMzgyMjI2In0sIngtbXMtc2d4LWVoZCI6IldtbW9mV25ReW5VM1IzY2dEZWNJVkxCc1hvMVVDZTBDSFpLWnYyZ1VKNXBxRkJHbjZHYW1NUT09IiwieC1tcy1zZ3gtaXMtZGVidWdnYWJsZSI6dHJ1ZSwieC1tcy1zZ3gtbXJlbmNsYXZlIjoiZTE2ZTM4MTg4ZTRiMGIwMDY5ODRlNjQzZDIzMzQxOTUyNjU4NDY4YzBjNmE3YzIzMzczMWIxZTUxMTIzOGYzMCIsIngtbXMtc2d4LW1yc2lnbmVyIjoiODNkNzE5ZTc3ZGVhY2ExNDcwZjZiYWY2MmE0ZDc3NDMwM2M4OTlkYjY5MDIwZjljNzBlZTFkZmMwOGM3Y2U5ZSIsIngtbXMtc2d4LXByb2R1Y3QtaWQiOjIsIngtbXMtc2d4LXJlcG9ydC1kYXRhIjoiOWU2Y2NkOTNjYjIwMGI5OTc3M2M2MDJiNDczNDRiMzA4OGU5MzU1ZTAwOGMzOGMyMTEwMTdlNGM0YzQ2NzViZDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAiLCJ4LW1zLXNneC1zdm4iOjAsImV4cCI6MTcxNzcxODIwMywianRpIjoiZDdjYTM2ODgtMDExMC00ZjAzLTk2MGYtMjE2NmU4NDMwMGUwIiwiaWF0IjoxNzE3NzE3OTAzLCJpc3MiOiJJbnRlbCBUcnVzdCBBdXRob3JpdHkiLCJuYmYiOjE3MTc3MTc5MDN9\
    .c3w1w46-lWS8i4Ro1ly_hRXV9mzWqTpo8FNjwIptcp-RTJ3ejz0MlL6uQYskeYB_U9Dy-4aOYjWEyjv7wsHc0J-zfukH_uY1-TYYRJVOF-JhxOkUpV0dwgXFKUYkYGBIs0VesyZP62K5S8eyMZ_e2MA7XWSskEIffqNw2ZYjE0LO1zcSI5Lts-uZCJbVyUcSPOeDj2nm0YFhRkmgj8guiMZ3-2WpV7CqJd6AmC7UFfSLhYiuOY0NWmZIB6yP2XNfsUXb_OgXLtw5CJ4xZ7T4zh_i-nahV5sjLk-wFR1C--LXwWmM91KvED6fpwT_XFgHZ4uiyrAzkM8WOyhOeKSPGo9tnQRlBVBACm7C39na-pA1qZrZLEZJrRfZcq3z8IyW05rU-MTgIp11rgv_cng-glSb4ckrRuCknJIX_0ccL6DP1xbIJVI9ju-DW59WHSClfVaOlG8lOIo0YCveIxhSi9d4AxmxhNTwn1W9p6FeepG5Q-PMJaQ_Zp2rzzBmiGzi";

    #[test]
    fn raw_key_conversion() {
        let raw_set: RawJsonWebKeySet = serde_json::from_str(RAW_KEY_SET).unwrap();
        let jwk_set: JsonWebKeySet = raw_set.try_into().unwrap();
        assert_eq!(jwk_set.keys.len(), 1);
    }

    #[test]
    fn token_validation() {
        let raw_set: RawJsonWebKeySet = serde_json::from_str(RAW_KEY_SET).unwrap();
        let jwks: JsonWebKeySet = raw_set.try_into().unwrap();
        let claims = validate_json_web_token(RAW_TOKEN.to_string(), jwks).unwrap();
        assert!(claims.x_ms_sgx_is_debuggable);
        assert_eq!(
            claims.x_ms_sgx_mrenclave,
            "e16e38188e4b0b006984e643d23341952658468c0c6a7c233731b1e511238f30"
        );
        assert_eq!(
            claims.x_ms_sgx_mrsigner,
            "83d719e77deaca1470f6baf62a4d774303c899db69020f9c70ee1dfc08c7ce9e"
        );
        let ehd = base64::engine::general_purpose::STANDARD
            .decode(&claims.x_ms_sgx_ehd)
            .unwrap();
        let hex: String = ehd.to_hex();
        assert_eq!(
            hex,
            "5a69a87d69d0ca75374777200de70854b06c5e8d5409ed021d9299bf6814279a6a1411a7e866a631",
        )
    }
}
