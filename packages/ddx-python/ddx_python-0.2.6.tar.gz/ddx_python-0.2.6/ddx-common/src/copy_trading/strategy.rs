use crate::{
    Result,
    crypto::{Keccak256, hash_without_prefix},
    global::Chain,
    impl_signing,
    types::{
        accounting::StrategyId as StrategyName,
        primitives::{Hash, Signature},
    },
    util::{
        eip712::{HashEIP712, Message, Payload, SignedEIP712},
        tokenize::Tokenizable,
    },
};
use ethereum_types::{Address, H520, U256};
use serde::{Deserialize, Serialize};
/// Represents a unique strategy (subaccount) identifier.
#[derive(
    Debug, Clone, Default, Serialize, Deserialize, std::hash::Hash, Eq, PartialEq, PartialOrd, Ord,
)]
#[serde(rename_all = "camelCase")]
pub struct StrategyId {
    /// Ethereum address of the strategy owner.
    pub leader_address: Address,
    /// Confidential pseudonym identifying the subaccount.
    ///
    /// This pseudonym may be a hash or lookup key linked to the subaccount's company ID.
    pub strategy_name: StrategyName,
}

impl StrategyId {
    pub fn new(leader_address: Address, strategy_name: String) -> Result<Self> {
        Ok(Self {
            leader_address,
            strategy_name: StrategyName::from_string(strategy_name)?,
        })
    }
}

impl Keccak256<Hash> for StrategyId {
    fn keccak256(&self) -> Hash {
        let pre_image = crate::ethabi::encode(&[
            self.leader_address.into_token(),
            self.strategy_name.into_token(),
        ]);
        hash_without_prefix(pre_image).into()
    }
}
/// Represents a request to bring a strategy online.
///
/// Leaders can use this request to create a new strategy or activate an existing one
/// by updating its API credentials.
#[derive(Debug, Serialize, Deserialize, Eq, PartialEq)]
#[serde(rename_all = "camelCase")]
pub struct RegisterStrategy {
    /// The name of the strategy to be activated.
    pub strategy_name: StrategyName,
    /// Authentication details for the exchange backend.
    /// Encrypted and base64 encoded as a string.
    pub auth: String,
    /// Unique nonce to prevent replay attacks.
    /// TODO: use nonce to verify the request
    nonce: U256,
    /// Ethereum signature of the request data for authenticity verification.
    signature: H520,
}

impl HashEIP712 for RegisterStrategy {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        let mut message = Message::new(chain, contract_address)?;
        let mut payload = Payload::from_signature(
            b"RegisterStrategy(bytes32 strategyName,bytes32 hashedAuth,uint256 nonce)".to_vec(),
        );
        // Since `KycRequest` contains String types, we will hash the string fields first.
        payload.append(self.strategy_name.0);
        // Ignore the auth field in the hash calculation since it is encrypted and too long to be converted to a token.
        payload.append(self.nonce);
        message.append_payload(payload);
        Ok(message.finalize())
    }
}

impl SignedEIP712 for RegisterStrategy {
    fn signature(&self) -> Signature {
        self.signature.into()
    }
}

impl RegisterStrategy {
    pub fn new(strategy_name: String, auth: String, nonce: U256) -> Result<RegisterStrategy> {
        Ok(Self {
            strategy_name: StrategyName::from_string(strategy_name)?,
            auth,
            nonce,
            signature: Default::default(),
        })
    }
}

impl_signing!(RegisterStrategy);

impl TryFrom<&RegisterStrategy> for StrategyId {
    type Error = anyhow::Error;

    fn try_from(strategy: &RegisterStrategy) -> anyhow::Result<Self> {
        // verify the registration request
        let (_hash, signer) = strategy.recover_signer()?;
        Ok(StrategyId {
            leader_address: signer.to_eth_address(),
            strategy_name: strategy.strategy_name,
        })
    }
}

/// Request to take a strategy offline.
///
/// Leaders use this request to deactivate a strategy.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct UnregisterStrategy {
    /// The name of the strategy to take offline.
    pub strategy_name: StrategyName,
    /// Unique nonce to prevent replay attacks.
    /// TODO: use nonce to verify the request
    pub nonce: U256,
    /// Ethereum signature of the request data.
    pub signature: H520,
}

impl HashEIP712 for UnregisterStrategy {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        let mut message = Message::new(chain, contract_address)?;
        let mut payload = Payload::from_signature(
            b"UnregisterStrategy(bytes32 strategyName,uint256 nonce)".to_vec(),
        );
        payload.append(self.strategy_name.0);
        payload.append(self.nonce);
        message.append_payload(payload);
        Ok(message.finalize())
    }
}

impl SignedEIP712 for UnregisterStrategy {
    fn signature(&self) -> Signature {
        self.signature.into()
    }
}

impl UnregisterStrategy {
    pub fn new(strategy_name: String, nonce: U256) -> Result<UnregisterStrategy> {
        Ok(Self {
            strategy_name: StrategyName::from_string(strategy_name)?,
            nonce,
            signature: Default::default(),
        })
    }
}

impl_signing!(UnregisterStrategy);

impl TryFrom<&UnregisterStrategy> for StrategyId {
    type Error = anyhow::Error;

    fn try_from(strategy: &UnregisterStrategy) -> anyhow::Result<Self> {
        // verify the un-registration request
        let (_hash, signer) = strategy.recover_signer()?;
        Ok(StrategyId {
            leader_address: signer.to_eth_address(),
            strategy_name: strategy.strategy_name,
        })
    }
}

#[cfg(test)]
mod tests {
    use base64::Engine;
    use libsecp256k1::SecretKey;
    use rand::RngCore;

    use crate::{
        constants::{AES_NONCE_LEN, SECRET_KEY_LEN},
        copy_trading::{Signing, auth::SubaccountAuth, test_account::read_binance_subaccounts},
        crypto::{EncryptedContent, decrypt, derive_pub_key, encrypt, sign_message},
    };

    use super::*;

    #[test]
    fn test_hash_register_strategy() {
        let register_strategy =
            RegisterStrategy::new("test".to_string(), "test".to_string(), U256::from(1)).unwrap();
        let _hash = register_strategy.hash_eip712().unwrap();
    }

    #[test]
    fn test_hash_unregister_strategy() {
        let unregister_strategy =
            UnregisterStrategy::new("test".to_string(), U256::from(1)).unwrap();
        let _hash = unregister_strategy.hash_eip712().unwrap();
    }

    #[test]
    fn test_serialize_register_strategy() {
        let auths = read_binance_subaccounts().unwrap();
        // encryption nonce
        let mut nonce_bytes = [0_u8; AES_NONCE_LEN];
        rand::thread_rng().try_fill_bytes(&mut nonce_bytes).unwrap();
        let mut network_secret_bytes = [0_u8; SECRET_KEY_LEN];
        rand::thread_rng()
            .try_fill_bytes(&mut network_secret_bytes)
            .unwrap();
        let network_secret_key = SecretKey::parse_slice(&network_secret_bytes).unwrap();
        let network_public_key = derive_pub_key(&network_secret_key);
        // encrypt the request
        let encrypted_content = encrypt(
            serde_json::to_vec(&auths[0]).unwrap(),
            &network_secret_bytes,
            &network_public_key.serialize_compressed(),
            nonce_bytes,
        )
        .unwrap();
        let encrypted_content_str =
            base64::engine::general_purpose::STANDARD.encode(encrypted_content);
        let register_strategy =
            RegisterStrategy::new("test".to_string(), encrypted_content_str, U256::from(1))
                .unwrap();
        // sign the request
        let signature = sign_message(
            &network_secret_key,
            register_strategy.hash_eip712().unwrap().into(),
        );
        let register_strategy = register_strategy.finalize(signature.unwrap());
        // serialize the request
        let serialized_request = serde_json::to_vec(&register_strategy).unwrap();
        // deserialize the request
        let deserialized_request: RegisterStrategy =
            serde_json::from_slice(&serialized_request).unwrap();
        // verify the deserialized request
        assert_eq!(register_strategy, deserialized_request);
        // take subaccount auth from the deserialized request
        let subaccount_bytes = base64::engine::general_purpose::STANDARD
            .decode(deserialized_request.auth)
            .unwrap();
        let encrypted_content = EncryptedContent::deserialize(subaccount_bytes).unwrap();
        // decrypt the subaccount auth
        let subaccount_auth = decrypt(encrypted_content, &network_secret_key).unwrap();
        // deserialize the subaccount auth
        let subaccount_auth: SubaccountAuth = serde_json::from_slice(&subaccount_auth).unwrap();
        // validate the subaccount auth
        assert_eq!(auths[0], subaccount_auth);
    }
}
