/// Ecall functions signatures for the enclave
use crate::constants::{
    ADDRESS_BYTE_LEN, COMPRESSED_KEY_BYTE_LEN, CUSTODIAN_ADDRESS_BYTE_LEN, USER_DATA_LEN,
};
use sgx_types::{
    error::SgxStatus,
    types::{EnclaveId, Report, TargetInfo},
};

extern "C" {
    // Attestation
    pub fn ecall_get_user_data(eid: EnclaveId, data: &mut [u8; USER_DATA_LEN]) -> SgxStatus;

    pub fn ecall_get_registration_report(
        eid: EnclaveId,
        retval: *mut SgxStatus,
        target_info: *const TargetInfo,
        report: *mut Report,
    ) -> SgxStatus;

    pub fn ecall_init_diagnostics(eid: EnclaveId, pretty_logs: bool) -> SgxStatus;

    pub fn ecall_get_signing_address(
        eid: EnclaveId,
        pubkey: &mut [u8; ADDRESS_BYTE_LEN],
    ) -> SgxStatus;

    pub fn ecall_get_encryption_key(
        eid: EnclaveId,
        compressed_key: &mut [u8; COMPRESSED_KEY_BYTE_LEN],
    ) -> SgxStatus;

    /// Initialize the enclave with the key parameters required for cryptography
    pub fn ecall_init_sealed(
        eid: EnclaveId,
        retval: *mut SgxStatus,
        sealed_in_ptr: *const u8,
        sealed_in_len: usize,
        custodian_address: &[u8; CUSTODIAN_ADDRESS_BYTE_LEN],
        sealed_out_ptr: *mut u8,
        out_max_len: usize,
        sealed_out_len: *mut usize,
    ) -> SgxStatus;

    /// Ensure the async runtime for the enclave is initialized
    pub fn ecall_init_runtime(eid: EnclaveId, retval: *mut SgxStatus) -> SgxStatus;
}
