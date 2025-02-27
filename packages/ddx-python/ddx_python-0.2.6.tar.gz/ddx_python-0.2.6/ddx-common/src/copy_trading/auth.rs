use serde::{Deserialize, Serialize};
use std::fmt;

use super::hash_without_prefix;
use crate::{crypto::Keccak256, types::primitives::Hash, util::tokenize::Tokenizable};

#[derive(Debug, Clone, Serialize, Deserialize, std::hash::Hash, Eq, PartialEq, PartialOrd, Ord)]
pub enum Exchange {
    Binance,
    Coinbase,
}

/// Represents the subaccount authentication request for each exchange backend.
///
/// This struct contains sensitive information required to authenticate the subaccount.
/// The authentication scheme varies between exchanges, which necessitates a flexible data model.
#[derive(Clone, Serialize, Deserialize, Eq, PartialEq)]
#[serde(tag = "type")]
#[serde(rename_all = "camelCase")]
pub enum SubaccountAuth {
    Binance {
        /// API key used to authenticate the subaccount on Binance.
        api_key: String,
        /// Exchange private key used for signing API messages on Binance.
        secret_key_pem: String,
        /// Identifier for the subaccount within the exchange's backend system.
        ///
        /// TODO: Clarify whether this field can be derived automatically or must always be explicitly provided.
        company_id: String,
    },
    /// Represents a Coinbase subaccount.
    // TODO: Not yet implemented.
    Coinbase,
    None,
}

impl Keccak256<Hash> for SubaccountAuth {
    fn keccak256(&self) -> Hash {
        match self {
            // Ignore the secret key in the hash since it is too long to be converted to a token.
            SubaccountAuth::Binance {
                api_key,
                company_id,
                ..
            } => {
                let pre_image = crate::ethabi::encode(&[
                    api_key.clone().into_token(),
                    company_id.clone().into_token(),
                ]);
                hash_without_prefix(pre_image).into()
            }
            SubaccountAuth::Coinbase => unimplemented!("No API key for Coinbase"),
            SubaccountAuth::None => panic!("No API key specified"),
        }
    }
}

impl fmt::Debug for SubaccountAuth {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            SubaccountAuth::Binance { api_key, .. } => f
                .debug_struct("SubaccountAuth::Binance")
                .field("api_key", &format!("{}...", &api_key[..5]))
                .field("secret_key_pem", &"hidden".to_string())
                .field("company_id", &"hidden".to_string())
                .finish(),
            SubaccountAuth::Coinbase => f.debug_struct("SubaccountAuth::Coinbase").finish(),
            SubaccountAuth::None => f.debug_struct("SubaccountAuth::None").finish(),
        }
    }
}

impl SubaccountAuth {
    pub fn binance(api_key: String, secret_key_pem: String, company_id: String) -> Self {
        SubaccountAuth::Binance {
            api_key,
            secret_key_pem,
            company_id,
        }
    }

    pub fn api_key(&self) -> &str {
        match self {
            SubaccountAuth::Binance { api_key, .. } => api_key,
            SubaccountAuth::Coinbase => unimplemented!("No API key for Coinbase"),
            SubaccountAuth::None => panic!("No API key specified"),
        }
    }

    pub fn exchange(&self) -> Exchange {
        match self {
            SubaccountAuth::Binance { .. } => Exchange::Binance,
            SubaccountAuth::Coinbase => Exchange::Coinbase,
            SubaccountAuth::None => panic!("No exchange specified"),
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::copy_trading::test_account::read_binance_subaccounts;

    use super::*;

    #[test]
    fn test_keccak256() {
        let auth =
            SubaccountAuth::binance("test".to_string(), "test".to_string(), "test".to_string());
        let test_hash = auth.keccak256();
        let auths = read_binance_subaccounts().unwrap();
        for auth in auths {
            let hash = auth.keccak256();
            assert_ne!(hash, test_hash);
        }
    }
}
