use ddx_common_macros::AbiToken;
#[cfg(feature = "database")]
use postgres_types::{FromSql, IsNull, ToSql, Type, to_sql_checked};
use serde::{Deserialize, Serialize};

#[cfg(not(target_family = "wasm"))]
pub mod clock;
#[cfg(not(target_vendor = "teaclave"))]
pub mod contract;
#[cfg(not(target_family = "wasm"))]
pub mod contract_events;
pub mod ethereum;

// Err on the side of supported all modes (sgx, std and wasm) for core types when doing so is practical.
// We want to expand logic exposed to the wasm library in the future, so the aim to minimize rework.
//
// This is not a strict rule, but a guideline, it makes sense to restrict the scope of more specialized
// types to avoid internal scoping of dependencies.
//
pub mod accounting;
pub mod checkpoint;
pub mod identifiers;
pub mod primitives;
pub mod request;
pub mod state;
pub mod transaction;

/// # Safety
/// Adding this trait means the marked struct uses contiguous memory.
/// It implies that the struct may be `memcpy` if using the same struct representation.
///
/// A macro rule for adding unsafe marker trait for struct.
#[cfg(not(target_family = "wasm"))]
#[macro_export]
macro_rules! impl_contiguous_marker_for {
    ($($ty:ty)*) => {
        $(
            unsafe impl $crate::util::mem::ContiguousMemory for $ty { }
        )*
    }
}

/// # Safety
/// The data type must use contiguous memory, which do not contain pointers.
///
/// A macro rule for unsafe byte slicing.
/// Using this macro to derive unsafe re-interpretation of a contiguous memory into and from a byte slice.
#[cfg(not(target_family = "wasm"))]
#[macro_export]
macro_rules! impl_unsafe_byte_slice_for {
    ($($ty:ty)*) => {
        $(
            unsafe impl $crate::util::mem::ByteSlice for $ty {
                unsafe fn to_byte_slice(self) -> [u8; std::mem::size_of::<$ty>()] {
                    std::mem::transmute::<$ty, [u8; std::mem::size_of::<$ty>()]>(self)
                }

                unsafe fn from_byte_slice(d: &[u8]) -> $ty {
                    let mut slice = [0; std::mem::size_of::<$ty>()];
                    // This method will check the length of the slice in runtime.
                    slice.copy_from_slice(d);
                    std::mem::transmute::<[u8; std::mem::size_of::<$ty>()], $ty>(slice)
                }
            }
        )*
    }
}

/// Supported chain variants
#[derive(
    Debug,
    Clone,
    Copy,
    Serialize,
    Deserialize,
    AbiToken,
    PartialEq,
    Eq,
    PartialOrd,
    Ord,
    std::hash::Hash,
)]
pub enum ChainVariant {
    Ethereum,
}

impl ChainVariant {
    #[cfg(feature = "database")]
    fn from_u8(n: u8) -> ChainVariant {
        match n {
            0 => ChainVariant::Ethereum,
            _ => panic!("Unexpected chain discriminant {:?}", n),
        }
    }

    #[cfg(not(target_family = "wasm"))]
    pub(crate) fn discriminant(&self) -> u8 {
        match self {
            ChainVariant::Ethereum => 0,
        }
    }
}

#[cfg(feature = "database")]
impl ToSql for ChainVariant {
    fn to_sql(
        &self,
        ty: &Type,
        out: &mut bytes::BytesMut,
    ) -> Result<IsNull, Box<dyn std::error::Error + 'static + Sync + Send>> {
        let value = self.discriminant() as i32;
        value.to_sql(ty, out)
    }

    fn accepts(ty: &Type) -> bool {
        <i32 as ToSql>::accepts(ty)
    }

    to_sql_checked!();
}

#[cfg(feature = "database")]
impl<'a> FromSql<'a> for ChainVariant {
    fn from_sql(
        ty: &Type,
        raw: &'a [u8],
    ) -> Result<Self, Box<dyn std::error::Error + Sync + Send>> {
        let discriminant: i32 = i32::from_sql(ty, raw)?;
        let result: Self = Self::from_u8(discriminant.try_into()?);
        Ok(result)
    }

    fn accepts(ty: &Type) -> bool {
        <i32 as FromSql>::accepts(ty)
    }
}
