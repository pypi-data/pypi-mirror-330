use crate::enclave::ecall::ecall_init_runtime;
use sgx_types::{error::SgxStatus, types::EnclaveId};

use super::ensure_ecall_success;

pub fn ensure_init_runtime(eid: EnclaveId) {
    let mut retval = SgxStatus::default();
    let status = unsafe { ecall_init_runtime(eid, &mut retval) };
    ensure_ecall_success(status, Some(retval)).unwrap();
}
