use tiny_keccak::keccak256;

use crate::{
    Result,
    constants::KECCAK256_DIGEST_SIZE,
    crypto::{Keccak256, public_key_address, recover, recover_public_key},
    ethereum_types::{Address, H256, U256},
    global::Chain,
    types::{
        primitives::{
            Bytes21, Bytes32, FixedBytesWrapper, Hash, SessionSignature, Signature, TraderAddress,
        },
        request::{
            AdminCmd, CancelAllIntent, CancelOrderIntent, DisasterRecovery, HttpsRequest,
            InsuranceFundWithdrawIntent, ModifyOrderIntent, OrderIntent, ProfileUpdate,
            WithdrawDDXIntent, WithdrawIntent,
        },
        transaction::MatchableIntent,
    },
};
#[cfg(not(target_family = "wasm"))]
use rustc_hex::ToHex;
use std::convert::TryFrom;

pub trait HashEIP712 {
    /// Computes the EIP-712 hash with no context
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash>;
    /// Computes the EIP-712 hash with the application context
    fn hash_eip712(&self) -> Result<Hash> {
        let context = crate::global::app_context();
        self.hash_eip712_raw(context.chain, context.contract_address)
    }
}

trait Signed1ctEIP712 {
    fn eip712_signature(&self) -> Signature;

    fn session_key_signature(&self) -> SessionSignature;
}

pub trait SignedEIP712: HashEIP712 {
    /// Returns the included signature
    fn signature(&self) -> Signature;

    /// Recovers the message hash and signer
    #[tracing::instrument(level = "debug", skip_all, fields(hash, signature, signer))]
    fn recover_signer(&self) -> Result<(Hash, Bytes21)> {
        let hash = self.hash_eip712()?;
        tracing::Span::current().record("hash", hash.to_string());
        let signature = self.signature();
        tracing::Span::current().record("signature", format!("{:?}", signature));
        let signer = TraderAddress::from(recover(hash.into(), signature.into())?);
        tracing::Span::current().record("signer", signer.to_string());
        Ok((hash, signer))
    }
}

pub trait MultisigEIP712: HashEIP712 {
    /// Returns the included signatures
    fn signatures(&self) -> Vec<Signature>;

    /// Recovers the message hash and signers
    fn recover_signers(&self) -> Result<(Hash, Vec<Bytes21>)> {
        let hash = self.hash_eip712()?;
        let signers = self
            .signatures()
            .into_iter()
            .map(|signature| recover(hash.into(), signature.into()))
            .collect::<Result<Vec<_>>>()?
            .iter()
            .map(Bytes21::from)
            .collect();
        Ok((hash, signers))
    }
}

pub struct Message(Vec<u8>);

impl Message {
    pub fn new(chain: Chain, contract_address: Address) -> Result<Self> {
        let mut message: Vec<u8> = Vec::new();
        // EIP191 header for EIP712 prefix
        message.extend_from_slice(b"\x19\x01");
        let mut domain_message: Vec<u8> = Vec::new();
        let eip712_domain_separator =
            b"EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"
                .keccak256();
        let domain_name_hash = b"DerivaDEX".keccak256();
        let domain_version_hash = b"1".keccak256();
        let Chain::Ethereum(chain_id) = chain;
        domain_message.extend_from_slice(eip712_domain_separator.as_ref());
        domain_message.extend_from_slice(domain_name_hash.as_ref());
        domain_message.extend_from_slice(domain_version_hash.as_ref());
        domain_message.extend_from_slice(&H256(U256::from(chain_id).into()).0);
        domain_message.extend_from_slice(Bytes32::from(contract_address).as_bytes());
        // Adding the domain header to the message
        let domain_hash = domain_message.keccak256();
        message.extend_from_slice(domain_hash.as_ref());
        Ok(Message(message))
    }

    pub fn append_payload(&mut self, payload: Payload) {
        self.0.extend_from_slice(payload.0.keccak256().as_ref());
    }

    pub fn finalize(&self) -> Hash {
        let bytes: [u8; KECCAK256_DIGEST_SIZE] = self.0.keccak256();
        Hash::from(bytes)
    }
}

pub struct Payload(Vec<u8>);

impl Payload {
    pub fn from_signature(abi_signature: Vec<u8>) -> Payload {
        let mut payload: Vec<u8> = Vec::new();
        let payload_separator_hash = abi_signature.keccak256();
        payload.extend_from_slice(payload_separator_hash.as_ref());
        Payload(payload)
    }

    pub fn append<F: Into<[u8; KECCAK256_DIGEST_SIZE]>>(&mut self, field: F) {
        self.0.extend_from_slice(&H256(field.into()).0);
    }
}

impl HashEIP712 for HttpsRequest {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        let mut message = Message::new(chain, contract_address)?;
        let mut payload = Payload::from_signature(b"KYCRequest(bytes32 requestHash)".to_vec());
        // Since `KycRequest` contains String types, we will hash the string fields first.
        let request_hash = self.keccak256();
        payload.append(request_hash);
        message.append_payload(payload);
        Ok(message.finalize())
    }
}

#[cfg(not(target_family = "wasm"))]
impl<T> SignedEIP712 for T
where
    T: Signed1ctEIP712 + HashEIP712,
{
    /// Returns the included signature
    fn signature(&self) -> Signature {
        self.eip712_signature()
    }

    /// Recovers the message hash and signer
    #[tracing::instrument(level = "debug", skip_all, fields(hash, signature, signer))]
    fn recover_signer(&self) -> Result<(Hash, Bytes21)> {
        // Get the session public key
        let hash = self.hash_eip712()?;
        tracing::Span::current().record("1CT intent hash", hash.to_string());
        let signature = self.signature();
        let initial_public_key = recover_public_key(&hash.into(), signature.into())?;
        tracing::debug!(
            ?initial_public_key,
            "initial public key recovered from 1CT intent",
        );

        // Get the trader address
        let session_key_signature = self.session_key_signature();
        let signer = if let Some(session_sig) = session_key_signature {
            tracing::debug!(
                "1CT intent was signed by a session key, need to recover the trader address still"
            );
            let session_signer_bytes = initial_public_key.serialize();
            // 1CT signs the session signer hex string as the message
            let session_signer_hex_string =
                format!("0x{}", session_signer_bytes.to_hex::<String>());
            let session_signer_hex_string_bytes = session_signer_hex_string.as_bytes();
            let mut eth_message = format!(
                "\x19Ethereum Signed Message:\n{}",
                session_signer_hex_string_bytes.len()
            )
            .into_bytes();
            eth_message.extend_from_slice(session_signer_hex_string_bytes);
            tracing::trace!("Hashing eth prefixes bytes {:?}", eth_message);
            let session_signer_hash = keccak256(&eth_message);
            TraderAddress::from(recover(session_signer_hash.into(), session_sig.into())?)
        } else {
            TraderAddress::from(public_key_address(initial_public_key))
        };
        tracing::debug!("signer recovered from 1CT intent {:?}", &signer.to_string());
        Ok((hash, signer))
    }
}

#[cfg(not(target_family = "wasm"))]
impl Signed1ctEIP712 for ModifyOrderIntent {
    fn eip712_signature(&self) -> Signature {
        self.signature
    }
    fn session_key_signature(&self) -> SessionSignature {
        self.session_key_signature
    }
}

impl HashEIP712 for ModifyOrderIntent {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        let mut message = Message::new(chain, contract_address)?;
        let mut payload = Payload::from_signature(
            b"ModifyOrderParams(bytes32 orderHash,bytes32 symbol,bytes32 strategy,uint256 side,uint256 orderType,bytes32 nonce,uint256 amount,uint256 price,uint256 stopPrice)"
                .to_vec(),
        );
        payload.append(Bytes32::from(self.order_hash));
        payload.append(Bytes32::from(self.symbol));
        payload.append(Bytes32::try_from(self.strategy)?);
        payload.append(U256::from(self.side as u8));
        payload.append(U256::from(u8::from(self.order_type)));
        payload.append(self.nonce);
        payload.append(U256::from(self.amount));
        payload.append(U256::from(self.price));
        payload.append(U256::from(self.stop_price));
        message.append_payload(payload);
        Ok(message.finalize())
    }
}

#[cfg(not(target_family = "wasm"))]
impl Signed1ctEIP712 for CancelOrderIntent {
    fn eip712_signature(&self) -> Signature {
        self.signature
    }

    fn session_key_signature(&self) -> SessionSignature {
        self.session_key_signature
    }
}

impl HashEIP712 for CancelOrderIntent {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        let mut message = Message::new(chain, contract_address)?;
        let mut payload = Payload::from_signature(
            b"CancelOrderParams(bytes32 symbol,bytes32 orderHash,bytes32 nonce)".to_vec(),
        );
        payload.append(Bytes32::from(self.symbol));
        payload.append(Bytes32::from(self.order_hash));
        payload.append(self.nonce);
        message.append_payload(payload);
        Ok(message.finalize())
    }
}

#[cfg(not(target_family = "wasm"))]
impl Signed1ctEIP712 for OrderIntent {
    fn eip712_signature(&self) -> Signature {
        self.signature
    }

    fn session_key_signature(&self) -> SessionSignature {
        self.session_key_signature
    }
}

impl HashEIP712 for OrderIntent {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        let mut message = Message::new(chain, contract_address)?;
        // TODO: Consider generating the signature using ethabi
        let mut payload = Payload::from_signature(b"OrderParams(bytes32 symbol,bytes32 strategy,uint256 side,uint256 orderType,bytes32 nonce,uint256 amount,uint256 price,uint256 stopPrice)".to_vec());
        // Addresses and strings must be resized to bytes32
        payload.append(Bytes32::from(self.symbol));
        payload.append(Bytes32::try_from(self.strategy)?);
        payload.append(U256::from(self.side as u8));
        payload.append(U256::from(u8::from(self.order_type)));
        payload.append(self.nonce);
        payload.append(U256::from(self.amount));
        payload.append(U256::from(self.price));
        payload.append(U256::from(self.stop_price));
        message.append_payload(payload);
        Ok(message.finalize())
    }
}

impl HashEIP712 for WithdrawDDXIntent {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        let mut message = Message::new(chain, contract_address)?;
        // TODO: Consider generating the signature using ethabi
        let mut payload =
            Payload::from_signature(b"WithdrawDDXParams(uint128 amount,bytes32 nonce)".to_vec());
        payload.append(U256::from(self.amount));
        payload.append(self.nonce);
        message.append_payload(payload);
        Ok(message.finalize())
    }
}

impl HashEIP712 for WithdrawIntent {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        let mut message = Message::new(chain, contract_address)?;
        // TODO: Consider generating the signature using ethabi
        let mut payload = Payload::from_signature(
            b"WithdrawParams(bytes32 strategyId,address currency,uint128 amount,bytes32 nonce)"
                .to_vec(),
        );
        // Addresses and strings must be resized to bytes32
        payload.append(Bytes32::try_from(self.strategy_id)?);
        payload.append(Bytes32::from(self.currency));
        payload.append(U256::from(self.amount));
        payload.append(self.nonce);
        message.append_payload(payload);
        Ok(message.finalize())
    }
}

impl HashEIP712 for InsuranceFundWithdrawIntent {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        let mut message = Message::new(chain, contract_address)?;
        // TODO: Consider generating the signature using ethabi
        let mut payload = Payload::from_signature(
            b"InsuranceFundWithdrawParams(address currency,uint128 amount,bytes32 nonce)".to_vec(),
        );
        // Addresses and strings must be resized to bytes32
        payload.append(Bytes32::from(self.currency));
        payload.append(U256::from(self.amount));
        payload.append(self.nonce);
        message.append_payload(payload);
        Ok(message.finalize())
    }
}

impl HashEIP712 for ProfileUpdate {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        let mut message = Message::new(chain, contract_address)?;
        let mut payload = Payload::from_signature(
            b"UpdateProfileParams(bool payFeesInDdx,bytes32 nonce)".to_vec(),
        );
        payload.append(U256::from(self.pay_fees_in_ddx as u8));
        payload.append(self.nonce);
        message.append_payload(payload);
        Ok(message.finalize())
    }
}

impl HashEIP712 for CancelAllIntent {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        let mut message = Message::new(chain, contract_address)?;
        let mut payload = Payload::from_signature(
            b"CancelAllParams(bytes32 symbol,bytes32 strategy,bytes32 nonce)".to_vec(),
        );
        payload.append(Bytes32::from(self.symbol));
        payload.append(Bytes32::try_from(self.strategy)?);
        payload.append(self.nonce);
        message.append_payload(payload);
        Ok(message.finalize())
    }
}

impl HashEIP712 for AdminCmd {
    /// Computes the EIP-712 hash
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        match self {
            AdminCmd::DisasterRecovery(DisasterRecovery { request_index, .. }) => {
                let mut message = Message::new(chain, contract_address)?;
                let mut payload = Payload::from_signature(
                    b"DisasterRecoveryParams(uint128 request_index)".to_vec(),
                );
                payload.append(U256::from(*request_index));
                message.append_payload(payload);
                Ok(message.finalize())
            }
        }
    }
}

impl MultisigEIP712 for AdminCmd {
    fn signatures(&self) -> Vec<Signature> {
        match self {
            AdminCmd::DisasterRecovery(DisasterRecovery { signatures, .. }) => signatures.clone(),
        }
    }
}

#[cfg(not(target_family = "wasm"))]
impl Signed1ctEIP712 for MatchableIntent {
    fn eip712_signature(&self) -> Signature {
        match self {
            Self::OrderIntent(intent) => intent.eip712_signature(),
            Self::ModifyOrderIntent(intent) => intent.eip712_signature(),
        }
    }

    fn session_key_signature(&self) -> SessionSignature {
        match self {
            Self::OrderIntent(intent) => intent.session_key_signature(),
            Self::ModifyOrderIntent(intent) => intent.session_key_signature(),
        }
    }
}

impl HashEIP712 for MatchableIntent {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        match self {
            Self::OrderIntent(intent) => intent.hash_eip712_raw(chain, contract_address),
            Self::ModifyOrderIntent(intent) => intent.hash_eip712_raw(chain, contract_address),
        }
    }
}

#[cfg(test)]
pub mod tests {
    use crate::types::{
        primitives::{OrderSide, TokenSymbol},
        request::{CancelOrderIntent, OrderIntent, OrderType, WithdrawDDXIntent, WithdrawIntent},
    };

    use super::HashEIP712;

    #[test]
    fn test_eip712_cancel_order() {
        let intent = CancelOrderIntent {
            symbol: Default::default(),
            order_hash: Default::default(),
            nonce: Default::default(),
            session_key_signature: Default::default(),
            signature: Default::default(),
        };
        assert_ne!(intent.hash_eip712().unwrap(), Default::default());
    }

    #[test]
    fn test_eip712_order() {
        let order_intent = OrderIntent {
            symbol: Default::default(),
            strategy: Default::default(),
            side: OrderSide::Bid,
            order_type: OrderType::Limit { post_only: false },
            nonce: Default::default(),
            amount: Default::default(),
            price: Default::default(),
            stop_price: Default::default(),
            session_key_signature: Default::default(),
            signature: Default::default(),
        };
        assert_ne!(order_intent.hash_eip712().unwrap(), Default::default());
    }

    #[test]
    fn test_eip712_withdraw_ddx() {
        let withdraw_ddx_intent = WithdrawDDXIntent {
            amount: Default::default(),
            nonce: Default::default(),
            signature: Default::default(),
        };
        assert_ne!(
            withdraw_ddx_intent.hash_eip712().unwrap(),
            Default::default()
        );
    }

    #[test]
    fn test_eip712_withdraw() {
        let withdraw_intent = WithdrawIntent {
            strategy_id: Default::default(),
            currency: TokenSymbol::USDC.into(),
            amount: Default::default(),
            nonce: Default::default(),
            signature: Default::default(),
        };
        assert_ne!(withdraw_intent.hash_eip712().unwrap(), Default::default());
    }
}
