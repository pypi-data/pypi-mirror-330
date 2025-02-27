#![feature(extract_if)]
#![feature(generic_const_exprs)]
#![feature(cfg_eval)]
#![feature(strict_provenance)]
#![allow(clippy::type_complexity)]
#![allow(clippy::too_many_arguments)]
#![allow(incomplete_features)]
#![allow(unexpected_cfgs)]
#![allow(non_local_definitions)]
// Allows this crate to refer to itself as ddx_common when using ddx_common_macros, which allows macros that need to bring this crate into scope to be used externally.
extern crate self as ddx_common;
#[cfg(target_vendor = "teaclave")]
extern crate sgx_types;

#[cfg(not(target_family = "wasm"))]
pub use crate::execution::error::*;
pub use ethabi;
pub use ethereum_types;

pub mod constants;
#[cfg(not(target_family = "wasm"))]
pub mod copy_trading;
pub mod crypto;
pub mod execution;
pub mod global;
pub mod specs;
#[cfg(not(target_family = "wasm"))]
pub mod tree;
#[cfg(not(target_family = "wasm"))]
pub(crate) mod trusted_settings;
pub mod types;
pub mod util;

pub mod error;
pub use crate::error::{Error, Result};

/// SGX remote attestation related modules
#[cfg(all(
    not(target_family = "wasm"),
    not(target_vendor = "teaclave"),
    feature = "sgx"
))]
pub mod attestation;
#[cfg(all(not(target_family = "wasm"), not(target_vendor = "teaclave")))]
pub mod core;
#[cfg(all(not(target_family = "wasm"), not(target_vendor = "teaclave")))]
pub mod db;
/// SGX untrusted code, including ecall signatures and ocall implementations
/// and helpers for the enclave
#[cfg(all(
    not(target_family = "wasm"),
    not(target_vendor = "teaclave"),
    feature = "sgx"
))]
pub mod enclave;
#[cfg(all(not(target_family = "wasm"), not(target_vendor = "teaclave")))]
pub mod node;
