use sgx_types::error::SgxStatus;
use std::mem::ManuallyDrop;

/// Copy the ecall outcome to the output pointer
/// # Safety
///
/// This function would deref a raw pointer as function arguments.
/// This function assumes the lifetime of the output pointer is valid.
/// This function does not drop the output vector.
#[no_mangle]
pub unsafe extern "C" fn ocall_copy_ecall_outcome(
    output_ptr: *const u8,
    output_init_cap: usize,
    output_addr: *mut usize,
    outcome_ptr: *const u8,
    outcome_len: usize,
) -> SgxStatus {
    let outcome = std::slice::from_raw_parts(outcome_ptr, outcome_len);
    // Safety: Does not destruct vector here.
    let mut output = ManuallyDrop::new(Vec::from_raw_parts(
        output_ptr as *mut u8,
        0,
        output_init_cap,
    ));
    output.extend_from_slice(outcome);
    if output_init_cap < outcome_len {
        // the outcome is too large to fit in the output buffer, so we need to reallocate
        *output_addr = output.as_ptr().addr();
    }
    SgxStatus::Success
}
