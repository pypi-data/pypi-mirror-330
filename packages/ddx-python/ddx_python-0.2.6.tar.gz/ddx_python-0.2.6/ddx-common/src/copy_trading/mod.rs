use ethereum_types::H520;
use serde::{Deserialize, Serialize};
use std::{fmt, ops::Deref, path::PathBuf};
use thiserror::Error;

use crate::{
    crypto::{Keccak256, hash_without_prefix},
    types::primitives::Hash,
    util::tokenize::Tokenizable,
};

pub mod auth;
pub mod execution;
pub mod strategy;
pub mod subscribe;
#[cfg(feature = "test_account")]
pub mod test_account;

/// The application directory as defined by convention.
///
/// This is a hard pre-requisite, as the application expects to find its configuration files in this directory.
pub fn certs_dir() -> PathBuf {
    let f = std::option_env!("CERTS_DIR").unwrap_or("/opt/dexlabs/certs");
    PathBuf::from(f)
        .canonicalize()
        .expect("Use the pre-configured docker image or configure your environment accordingly")
}

#[derive(Error, Debug, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "camelCase")]
#[serde(tag = "type")]
pub enum ValueError {
    #[error("Failed to parse the FIX message: {error}")]
    ParsingError { error: String },
    #[allow(unused)]
    #[error("Failed to encode the FIX message: {error}")]
    EncodingError { error: String },
    #[error("Error due to invalid application configuration: {error}")]
    ConfigurationError { error: String },
    #[error("Failed to serialize the event: {error}")]
    SerializationError { error: String },
    #[error("Other error: {error}")]
    Other { error: String },
}

#[derive(Error, Debug, Serialize)]
#[serde(rename_all = "camelCase")]
#[serde(tag = "type")]
pub enum CryptoError {
    #[error("Failed to parse PEM keys: {error}")]
    ParsingError { error: String },
    #[error("Failed to decode as Ed25519 key pair: {error}")]
    InvalidKeyPair { error: String },
}

/// Errors that cannot be resolved internally and require user action.
///
/// These errors are intended to be dispatched to the user interface for resolution.
/// Unlike `SessionException`, this is kept high-level to avoid noise or revealing sensitive info.
// TODO: Align with SessionStatus for robust frontend behavior.
#[derive(Error, Debug, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "camelCase")]
#[serde(tag = "type")]
pub enum SessionNotice {
    #[error("FIX logon rejected; {error}")]
    AuthenticationError { error: String },
    // TODO: Replace this with the more useful RejectMessage like SessionStatus.
    #[error("FIX message skipped; {0}")]
    #[serde(untagged)]
    ValueError(#[from] ValueError),
}

pub trait Signing {
    fn finalize(self, signature: H520) -> Self;
}

#[macro_export]
macro_rules! impl_signing {
    ($type:ty) => {
        impl ddx_common::copy_trading::Signing for $type {
            fn finalize(self, signature: H520) -> Self {
                Self { signature, ..self }
            }
        }
    };
}

/// Symbol helper to abstract the exchange specific symbol representation.
#[derive(Debug, Default, Clone, Hash, Eq, PartialEq, Serialize, Deserialize)]
pub struct Symbol(pub String);

impl Keccak256<Hash> for Symbol {
    fn keccak256(&self) -> Hash {
        let pre_image = crate::ethabi::encode(&[self.0.clone().into_token()]);
        hash_without_prefix(pre_image).into()
    }
}

impl fmt::Display for Symbol {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl Deref for Symbol {
    type Target = String;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl From<String> for Symbol {
    fn from(symbol: String) -> Self {
        Symbol(symbol)
    }
}

impl From<&str> for Symbol {
    fn from(symbol: &str) -> Self {
        Symbol(symbol.to_string())
    }
}

impl Symbol {
    pub fn new<T: ToString>(symbol: T) -> Self {
        Symbol(symbol.to_string())
    }

    pub fn is_quote_usd(&self) -> bool {
        self.ends_with("USDT") || self.ends_with("BUSD")
    }
}
