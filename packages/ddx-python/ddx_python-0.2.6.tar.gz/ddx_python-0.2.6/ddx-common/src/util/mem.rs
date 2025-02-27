use anyhow::Result;
use serde::Serialize;
use std::mem::size_of;

/// # Safety
///
/// This trait should be only used for types with contiguous memory.
pub unsafe trait ContiguousMemory {}

/// # Safety
///
/// This trait should be only used for types with contiguous memory.
///
/// An unsafe trait to convert a type with contiguous memory from and to a byte slice.
pub unsafe trait ByteSlice: Sized + ContiguousMemory {
    /// # Safety
    ///
    /// The struct is converted into a byte slice
    unsafe fn to_byte_slice(self) -> [u8; size_of::<Self>()];
    /// # Safety
    ///
    /// The byte slice argument must have equal or longer length than the size of the resulted struct.
    unsafe fn from_byte_slice(d: &[u8]) -> Self;
}

/// # Safety
///
/// This trait should be only used for copying data from/to trusted memory to/from untrusted memory.
///
/// An unsafe trait to copy a struct between trusted memory and untrusted memory.
pub unsafe trait MemCopy {
    /// # Safety
    ///
    /// The struct is copied into another struct.
    ///
    /// The destination pointer must be valid and have enough space to store the struct.
    unsafe fn mem_copy(self, buffer: *mut u8, size: usize) -> Result<usize>;
}

unsafe impl<T> MemCopy for T
where
    T: ByteSlice,
    [(); size_of::<Self>()]:,
{
    unsafe fn mem_copy(self, dst: *mut u8, size: usize) -> Result<usize> {
        let src = self.to_byte_slice();
        let count = src.len();
        if count > size {
            return Err(anyhow::anyhow!(
                "The destination buffer is too small to store the struct."
            ));
        }
        std::ptr::copy_nonoverlapping(src.as_ptr(), dst, count);
        Ok(count)
    }
}

/// # Safety
///
/// This trait should be only used for serializing data from/to trusted memory to/from untrusted memory.
///
/// An unsafe trait to copy a serialized struct between trusted memory and untrusted memory.
pub unsafe trait SerializedCopy {
    /// # Safety
    ///
    /// The struct is copied into another struct.
    ///
    /// The destination pointer must be valid and have enough space to store the struct.
    unsafe fn serialized_copy(self, buffer: *mut u8, size: usize) -> Result<usize>;
}

unsafe impl<T> SerializedCopy for T
where
    T: Serialize,
{
    unsafe fn serialized_copy(self, dst: *mut u8, size: usize) -> Result<usize> {
        let serialized = serde_cbor::to_vec(&self)?;
        let count = serialized.len();
        if count > size {
            return Err(anyhow::anyhow!(
                "The destination buffer is too small to store the struct."
            ));
        }
        std::ptr::copy_nonoverlapping(serialized.as_ptr(), dst, count);
        Ok(count)
    }
}
