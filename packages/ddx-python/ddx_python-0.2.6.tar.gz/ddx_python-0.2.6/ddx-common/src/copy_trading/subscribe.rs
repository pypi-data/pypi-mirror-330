use crate::{
    Result,
    crypto::{Keccak256, recover},
    global::Chain,
    impl_signing,
    types::primitives::{Hash, Signature},
    util::eip712::{HashEIP712, Message, Payload, SignedEIP712},
};
use ethereum_types::{Address, H520};
use serde::{Deserialize, Serialize};

use super::strategy::StrategyId;

/// Represents a request to register a trader
#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
#[repr(C)]
pub struct LogonRequest {
    /// The list of strategy ids to subscribe to
    pub strategy_ids: Vec<StrategyId>,
    /// Ethereum signature of the request data for authenticity verification.
    signature: H520,
}

impl LogonRequest {
    pub fn new(strategy_ids: Vec<StrategyId>) -> Self {
        Self {
            strategy_ids,
            signature: H520::default(),
        }
    }

    pub fn signer_address(&self) -> Result<Address> {
        let hash = self.hash_eip712()?;
        let sig = self.signature();
        recover(hash.into(), sig.into())
    }
}

impl_signing!(LogonRequest);

impl HashEIP712 for LogonRequest {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        let mut message = Message::new(chain, contract_address)?;
        let mut payload = Payload::from_signature(
            b"RegisterTrader(uint256 subscriptionFee,uint256 subscriptionBlockDelta)".to_vec(),
        );
        for strategy_id in self.strategy_ids.iter() {
            payload.append(strategy_id.keccak256());
        }
        message.append_payload(payload);
        Ok(message.finalize())
    }

    fn hash_eip712(&self) -> Result<Hash> {
        let context = crate::global::app_context();
        self.hash_eip712_raw(context.chain, context.contract_address)
    }
}

impl SignedEIP712 for LogonRequest {
    fn signature(&self) -> Signature {
        self.signature.into()
    }
}

/// Represents a response to a logon request
#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct LogonResponse {
    /// The number of strategies subscribed to
    pub strategy_count: usize,
}
