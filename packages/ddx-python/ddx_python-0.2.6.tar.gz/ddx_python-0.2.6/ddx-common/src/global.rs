#[cfg(feature = "python")]
use pyo3::prelude::*;
#[cfg(feature = "python")]
use rustc_hex::ToHex;

use crate::{
    ethereum_types::Address,
    types::{ChainVariant, ethereum::DeploymentMeta, primitives::TokenSymbol},
};
use ddx_common_macros::AbiToken;
use lazy_static::lazy_static;
use serde::{Deserialize, Serialize};
use std::{
    collections::HashMap,
    sync::{RwLock, RwLockReadGuard},
};

/// Supported chain variants with the environment identifier
#[derive(Debug, Copy, Clone, Serialize, Deserialize, AbiToken, PartialEq)]
pub enum Chain {
    /// Ethereum contains a chain_id to identify the network
    Ethereum(u64),
}

impl Chain {
    pub fn variant(&self) -> ChainVariant {
        match self {
            Chain::Ethereum(_) => ChainVariant::Ethereum,
        }
    }
}

cfg_if::cfg_if! {
    if #[cfg(not(target_family = "wasm"))] {
        lazy_static! {
            /// Loads the application from the environment by convention.
            static ref APP_CONTEXT: RwLock<ApplicationContext> = RwLock::new(ApplicationContext::from_env());
        }
    } else {
        lazy_static! {
            /// Loads an uninitialized application context that requires manual initialization.
            ///
            /// This is useful for sandboxed environments where the environment variables are not available.
            /// It may also be useful for testing although tests do not generally require exotic app context configurations.
            ///
            static ref APP_CONTEXT: RwLock<ApplicationContext> = RwLock::new(ApplicationContext {
                contract_address: Default::default(),
                collateral_addresses: HashMap::with_capacity(1),
                ddx_token_address: Default::default(),
                chain: Chain::Ethereum(Default::default()),
                initialized: false
            });
        }
    }
}

/// Initialize the app context by passing it in.
///
/// This is useful in sandboxed context without environment access.
///
/// Note that setting the app context here does not propagate to the enclave.
pub fn init_app_context(context: ApplicationContext) {
    let mut app_context = APP_CONTEXT.write().unwrap();
    assert!(!app_context.initialized, "App context already initalized");
    *app_context = context;
    app_context.initialized = true;
}

/// Holds application-layer environment information
///
/// Information in here as analogous to something like the operating system locale, but at the application layer.
/// In the git application for instance, such context includes name and email.
/// Storing this information globally saves us the noise of repeating the same informational arguments
/// in multiple functions throughout the application.
///
/// This does NOT include logic inputs of individual units like configuration parameters (like db credentials),
/// business rules (like epoch sizes), etc. We capture these in `TrustedContext` and `NodeContext`, and
/// pass them explicitly to individual components (in the name of functional testability).
///
/// This information does not impact logic routes (testability)
#[cfg_attr(feature = "python", pyclass(frozen, name = "OperatorContext"))]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApplicationContext {
    pub contract_address: Address,
    pub collateral_addresses: HashMap<TokenSymbol, Address>,
    pub ddx_token_address: Address,
    /// Unsecure mode that disables sequencer signature validation when executing requests
    pub chain: Chain,
    initialized: bool,
}

#[cfg(feature = "python")]
#[pymethods]
impl ApplicationContext {
    #[getter]
    fn contract_address(&self) -> String {
        format!("0x{}", self.contract_address.0.to_hex::<String>())
    }

    #[getter]
    fn chain_id(&self) -> u64 {
        match self.chain {
            Chain::Ethereum(id) => id,
        }
    }
}

impl ApplicationContext {
    pub fn from_env() -> Self {
        let meta = DeploymentMeta::from_env();
        Self {
            chain: Chain::Ethereum(meta.chain_id),
            contract_address: meta.addresses.derivadex,
            collateral_addresses: vec![(TokenSymbol::USDC, meta.addresses.usdc_token)]
                .into_iter()
                .collect(),
            ddx_token_address: meta.addresses.ddx_token,
            initialized: true,
        }
    }
}

pub fn app_context() -> RwLockReadGuard<'static, ApplicationContext> {
    let context = APP_CONTEXT.read().unwrap();
    assert!(
        context.initialized,
        "App context not initialized; call init_app_context() first"
    );
    context
}
