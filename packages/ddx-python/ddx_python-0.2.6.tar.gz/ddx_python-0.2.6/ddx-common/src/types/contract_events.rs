use crate::{
    Result, bail,
    ddx_common::ethereum_types::{H256, U128, U256},
    ensure, error,
    ethabi::{Event, EventParam, Log, ParamType, RawLog},
    specs::types::{SpecsExpr, SpecsKey, SpecsUpdate},
    types::{
        accounting::{MAIN_STRAT, StrategyId},
        ethereum::LogEntry,
        identifiers::{
            InsuranceFundContributorAddress, ReleaseHash, SignerAddress, StrategyIdHash,
        },
        primitives::{
            Bytes32, FixedBytesWrapper, Hash, RecordedAmount, TokenAddress, TraderAddress,
        },
        state::VoidableItem,
        transaction::{
            BlockTxStamp, CheckpointConfirmed, InsuranceFundUpdate, InsuranceFundUpdateKind,
            StrategyUpdate, StrategyUpdateKind, TraderUpdate, TraderUpdateKind,
        },
    },
    util::tokenize::Tokenizable,
};
use ddx_common_macros::{AbiToken, EventDefinition};
use lazy_static::lazy_static;
use serde::{Deserialize, Serialize};
use std::convert::TryFrom;

use super::primitives::EpochId;

const SPECS_UPDATED_EVENT: &str = "SpecsUpdated";
const STRATEGY_UPDATED_EVENT: &str = "StrategyUpdated";
const TRADER_UPDATED_EVENT: &str = "TraderUpdated";
const INSURANCE_FUND_UPDATED_EVENT: &str = "FundedInsuranceFundUpdated";
const CHECKPOINT_APPROVED_EVENT: &str = "Checkpointed";
const SIGNER_REGISTERED: &str = "SignerRegistered";
const RELEASE_SCHEDULE_UPDATED_EVENT: &str = "ReleaseScheduleUpdated";

lazy_static! {
    static ref SPECS_UPDATED_EVENT_SIGNATURE: H256 = SpecsUpdatedEvent::default().signature();
    static ref STRATEGY_UPDATED_EVENT_SIGNATURE: H256 = StrategyUpdatedEvent::default().signature();
    static ref TRADER_UPDATED_EVENT_SIGNATURE: H256 = TraderUpdatedEvent::default().signature();
    static ref INSURANCE_FUND_UPDATED_EVENT_SIGNATURE: H256 =
        InsuranceFundUpdatedEvent::default().signature();
    static ref CHECKPOINT_APPROVED_EVENT_SIGNATURE: H256 = CheckpointedEvent::default().signature();
    static ref SIGNER_REGISTERED_EVENT_SIGNATURE: H256 =
        SignerRegisteredEvent::default().signature();
    static ref RELEASE_SCHEDULE_UPDATED_EVENT_SIGNATURE: H256 =
        ReleaseScheduleUpdatedEvent::default().signature();
}

pub(crate) trait EventDefinition {
    fn signature(&self) -> H256;
}

pub(crate) fn all_event_signatures() -> Vec<H256> {
    vec![
        *SPECS_UPDATED_EVENT_SIGNATURE,
        *STRATEGY_UPDATED_EVENT_SIGNATURE,
        *TRADER_UPDATED_EVENT_SIGNATURE,
        *INSURANCE_FUND_UPDATED_EVENT_SIGNATURE,
        *CHECKPOINT_APPROVED_EVENT_SIGNATURE,
        *SIGNER_REGISTERED_EVENT_SIGNATURE,
        *RELEASE_SCHEDULE_UPDATED_EVENT_SIGNATURE,
    ]
}

pub(crate) fn decode_contract_events(log: LogEntry) -> Vec<ContractEvent> {
    if !log.topics.is_empty() {
        let signature = log.topics[0];
        if signature == *SPECS_UPDATED_EVENT_SIGNATURE {
            SpecsUpdate::from_log(log)
                .map(ContractEvent::SpecsUpdate)
                .ok()
        } else if signature == *STRATEGY_UPDATED_EVENT_SIGNATURE {
            StrategyUpdate::from_log(log)
                .map(ContractEvent::StrategyUpdate)
                .ok()
        } else if signature == *TRADER_UPDATED_EVENT_SIGNATURE {
            TraderUpdate::from_log(log)
                .map(ContractEvent::TraderUpdate)
                .ok()
        } else if signature == *INSURANCE_FUND_UPDATED_EVENT_SIGNATURE {
            InsuranceFundUpdate::from_log(log)
                .map(ContractEvent::InsuranceFundUpdate)
                .ok()
        } else if signature == *CHECKPOINT_APPROVED_EVENT_SIGNATURE {
            CheckpointConfirmed::from_log(log)
                .map(ContractEvent::Checkpointed)
                .ok()
        } else if signature == *SIGNER_REGISTERED_EVENT_SIGNATURE {
            SignerRegisteredMeta::from_log(log)
                .map(ContractEvent::SignerRegistered)
                .ok()
        } else if signature == *RELEASE_SCHEDULE_UPDATED_EVENT_SIGNATURE {
            ReleaseUpdate::from_log(log)
                .map(ContractEvent::ReleaseScheduleUpdated)
                .ok()
        } else {
            None
        }
    } else {
        None
    }
    .map_or(vec![], |e| vec![e])
}

#[derive(Debug, Clone, PartialEq, EventDefinition)]
struct SpecsUpdatedEvent(pub Event);

impl Default for SpecsUpdatedEvent {
    fn default() -> Self {
        SpecsUpdatedEvent(Event {
            name: SPECS_UPDATED_EVENT.to_string(),
            inputs: vec![
                EventParam {
                    name: "key".to_string(),
                    kind: ParamType::FixedBytes(30),
                    indexed: true,
                },
                EventParam {
                    name: "specs".to_string(),
                    kind: ParamType::String,
                    indexed: false,
                },
                EventParam {
                    name: "op".to_string(),
                    kind: ParamType::Uint(8),
                    indexed: false,
                },
            ],
            anonymous: false,
        })
    }
}

#[derive(Debug, Clone, PartialEq, EventDefinition)]
struct StrategyUpdatedEvent(pub Event);

impl Default for StrategyUpdatedEvent {
    fn default() -> Self {
        StrategyUpdatedEvent(Event {
            name: STRATEGY_UPDATED_EVENT.to_string(),
            inputs: vec![
                EventParam {
                    name: "trader".to_string(),
                    kind: ParamType::Address,
                    indexed: true,
                },
                EventParam {
                    name: "collateralAddress".to_string(),
                    kind: ParamType::Address,
                    indexed: true,
                },
                EventParam {
                    name: "strategyIdHash".to_string(),
                    kind: ParamType::FixedBytes(4),
                    indexed: true,
                },
                EventParam {
                    name: "strategyId".to_string(),
                    kind: ParamType::FixedBytes(32),
                    indexed: false,
                },
                EventParam {
                    name: "amount".to_string(),
                    kind: ParamType::Uint(128),
                    indexed: false,
                },
                EventParam {
                    name: "updateType".to_string(),
                    kind: ParamType::Uint(8),
                    indexed: false,
                },
            ],
            anonymous: false,
        })
    }
}

#[derive(Debug, Clone, PartialEq, EventDefinition)]
struct TraderUpdatedEvent(pub Event);

impl Default for TraderUpdatedEvent {
    fn default() -> Self {
        TraderUpdatedEvent(Event {
            name: TRADER_UPDATED_EVENT.to_string(),
            inputs: vec![
                EventParam {
                    name: "trader".to_string(),
                    kind: ParamType::Address,
                    indexed: true,
                },
                EventParam {
                    name: "amount".to_string(),
                    kind: ParamType::Uint(128),
                    indexed: false,
                },
                EventParam {
                    name: "updateType".to_string(),
                    kind: ParamType::Uint(8),
                    indexed: false,
                },
            ],
            anonymous: false,
        })
    }
}

#[derive(Debug, Clone, PartialEq, EventDefinition)]
struct CheckpointedEvent(pub Event);

impl Default for CheckpointedEvent {
    fn default() -> Self {
        CheckpointedEvent(Event {
            name: CHECKPOINT_APPROVED_EVENT.to_string(),
            inputs: vec![
                EventParam {
                    name: "stateRoot".to_string(),
                    kind: ParamType::FixedBytes(32),
                    indexed: true,
                },
                EventParam {
                    name: "transactionRoot".to_string(),
                    kind: ParamType::FixedBytes(32),
                    indexed: true,
                },
                EventParam {
                    name: "epochId".to_string(),
                    kind: ParamType::Uint(128),
                    indexed: true,
                },
                EventParam {
                    name: "custodians".to_string(),
                    kind: ParamType::Array(Box::new(ParamType::Address)),
                    indexed: false,
                },
                EventParam {
                    name: "bonds".to_string(),
                    kind: ParamType::Array(Box::new(ParamType::Uint(128))),
                    indexed: false,
                },
                EventParam {
                    name: "submitter".to_string(),
                    kind: ParamType::Address,
                    indexed: false,
                },
            ],
            anonymous: false,
        })
    }
}

#[derive(Debug, Clone, PartialEq, EventDefinition)]
struct InsuranceFundUpdatedEvent(pub Event);

impl Default for InsuranceFundUpdatedEvent {
    fn default() -> Self {
        InsuranceFundUpdatedEvent(Event {
            name: INSURANCE_FUND_UPDATED_EVENT.to_string(),
            inputs: vec![
                EventParam {
                    name: "contributor".to_string(),
                    kind: ParamType::Address,
                    indexed: true,
                },
                EventParam {
                    name: "collateralAddress".to_string(),
                    kind: ParamType::Address,
                    indexed: true,
                },
                EventParam {
                    name: "amount".to_string(),
                    kind: ParamType::Uint(128),
                    indexed: false,
                },
                EventParam {
                    name: "updateKind".to_string(),
                    kind: ParamType::Uint(8),
                    indexed: false,
                },
            ],
            anonymous: false,
        })
    }
}

#[derive(Debug, Clone, PartialEq, EventDefinition)]
struct SignerRegisteredEvent(pub Event);

impl Default for SignerRegisteredEvent {
    fn default() -> Self {
        SignerRegisteredEvent(Event {
            name: SIGNER_REGISTERED.to_string(),
            inputs: vec![
                EventParam {
                    name: "releaseHash".to_string(),
                    kind: ParamType::FixedBytes(32),
                    indexed: true,
                },
                EventParam {
                    name: "custodian".to_string(),
                    kind: ParamType::Address,
                    indexed: true,
                },
                EventParam {
                    name: "signer".to_string(),
                    kind: ParamType::Address,
                    indexed: true,
                },
            ],
            anonymous: false,
        })
    }
}

#[derive(Debug, Clone, PartialEq, EventDefinition)]
struct ReleaseScheduleUpdatedEvent(pub Event);

impl Default for ReleaseScheduleUpdatedEvent {
    fn default() -> Self {
        ReleaseScheduleUpdatedEvent(Event {
            name: RELEASE_SCHEDULE_UPDATED_EVENT.to_string(),
            inputs: vec![
                EventParam {
                    name: "mrEnclave".to_string(),
                    kind: ParamType::FixedBytes(32),
                    indexed: true,
                },
                EventParam {
                    name: "isvSvn".to_string(),
                    kind: ParamType::FixedBytes(2),
                    indexed: true,
                },
                EventParam {
                    name: "startingEpochId".to_string(),
                    kind: ParamType::Uint(128),
                    indexed: true,
                },
            ],
            anonymous: false,
        })
    }
}

/// All possible relevant events emitted by the smart contract
// TODO 3591: Standardize event common attributes (tx_hash, block_number, etc). Giving the block number to `ParseLog::from_log` is probably easiest.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum ContractEvent {
    SpecsUpdate(SpecsUpdate),
    // TODO 3591: The idea is that we capture the event data into this raw type, and then enrich it with metadata. Make sure this isn't error prone given the use of default values.
    StrategyUpdate(StrategyUpdate<RecordedAmount>),
    TraderUpdate(TraderUpdate<RecordedAmount>),
    InsuranceFundUpdate(InsuranceFundUpdate<RecordedAmount>),
    BalanceTransfer,
    WithdrawConfirmed,
    Checkpointed(CheckpointConfirmed),
    SignerRegistered(SignerRegisteredMeta),
    ReleaseScheduleUpdated(ReleaseUpdate),
}

pub trait ParseLog {
    fn from_log(value: LogEntry) -> Result<Self>
    where
        Self: Sized;
}

fn parse_event_log(event: Event, log: RawLog) -> std::result::Result<Log, ethabi::Error> {
    event.parse_log(log)
}

impl ParseLog for SpecsUpdate {
    fn from_log(log: LogEntry) -> Result<Self> {
        // Web3/ethabi gyrations to parse the event into a structured log
        let raw_log = RawLog {
            topics: log.topics.clone(),
            data: log.data,
        };
        let event_ = SpecsUpdatedEvent::default();
        let log_ = parse_event_log(event_.0, raw_log)?;
        let mut iter = log_.params.into_iter();

        let key_param = iter
            .find(|p| p.name.as_str() == "key")
            .ok_or_else(|| error!("Expected specs key"))?;
        let key = SpecsKey::from_token(key_param.value)?;

        let specs_param = iter
            .find(|p| p.name.as_str() == "specs")
            .ok_or_else(|| error!("Expected specs expression"))?;

        let op_param = iter
            .find(|p| p.name.as_str() == "op")
            .ok_or_else(|| error!("Expected op variant"))?;
        let op = op_param
            .value
            .into_uint()
            .ok_or_else(|| error!("Expected int op discriminant"))?;

        let specs = SpecsExpr::from_token(specs_param.value)?;
        // Matching enum: `enum SpecsUpdateType { Upsert, Remove }`
        if op == U256::zero() {
            ensure!(specs.is_some(), "Got upsert op but the expression is empty");
            Ok(SpecsUpdate {
                key,
                expr: specs,
                block_number: Default::default(),
                tx_hash: log.tx_hash.into(),
            })
        } else if op == U256::one() {
            ensure!(specs.is_void(), "Got remove op but an expression was given");
            Ok(SpecsUpdate {
                key,
                expr: specs,
                block_number: Default::default(),
                tx_hash: log.tx_hash.into(),
            })
        } else {
            Err(error!(
                "Unexpected specs update operation discriminant {:?}",
                op
            ))
        }
    }
}

impl ParseLog for StrategyUpdate<RecordedAmount> {
    fn from_log(log: LogEntry) -> Result<Self> {
        // Web3/ethabi gyrations to parse the event into a structured log
        let raw_log = RawLog {
            topics: log.topics.clone(),
            data: log.data,
        };
        let strategy_event = StrategyUpdatedEvent::default();
        let log_ = parse_event_log(strategy_event.0, raw_log)?;
        let mut event = StrategyUpdate::default();
        for param in log_.params {
            // It's safe to unwrap here because we know the rules by construction
            match param.name.as_str() {
                "trader" => event.trader = param.value.into_address().unwrap().into(),
                "collateralAddress" => {
                    event.collateral_address =
                        TokenAddress::collateral(param.value.into_address().unwrap())
                }
                "strategyIdHash" => {
                    event.strategy_id_hash =
                        StrategyIdHash::from_slice(&param.value.into_fixed_bytes().unwrap())
                }
                "strategyId" => {
                    // If we aren't using multiple strategies, then set the strategy id to main
                    // Otherwise use what came from the contract
                    // TODO: once we enable multiple strategies remove this condition, we will
                    // use the contract event strategy unless it isn't valid utf8
                    let raw_value = Bytes32::from_slice(&param.value.into_fixed_bytes().unwrap());
                    event.strategy_id = if raw_value == Bytes32::default() {
                        None
                    } else {
                        Some(if cfg!(feature = "multi_strategies") {
                            raw_value.into()
                        } else {
                            StrategyId::from_string(MAIN_STRAT.into()).unwrap()
                        })
                    };
                }
                "amount" => {
                    event.amount = U128::try_from(param.value.into_uint().unwrap())
                        .unwrap()
                        .into()
                }
                "updateType" => {
                    event.update_kind = StrategyUpdateKind::try_from(
                        param.value.into_uint().unwrap().low_u32() as u8,
                    )?
                }
                _ => bail!("Unexpected param for StrategyUpdate {:?}", param),
            }
        }
        event.tx_stamp = Some(BlockTxStamp {
            block_number: 0,
            tx_hash: log.tx_hash.into(),
        });
        Ok(event)
    }
}

impl ParseLog for TraderUpdate<RecordedAmount> {
    fn from_log(log: LogEntry) -> Result<Self> {
        let raw_log = RawLog {
            topics: log.topics.clone(),
            data: log.data,
        };
        let trader_event = TraderUpdatedEvent::default();
        let log_ = parse_event_log(trader_event.0, raw_log)?;
        let mut event = TraderUpdate::default();
        for param in log_.params {
            match param.name.as_str() {
                "trader" => {
                    event.trader = param.value.into_address().unwrap().into();
                }
                "amount" => {
                    // DDX value has already been appropriately scaled down on the contract side, so no need to scale down here.
                    event.amount = Some(
                        U128::try_from(param.value.into_uint().unwrap())
                            .unwrap()
                            .into(),
                    );
                }
                "updateType" => {
                    event.update_kind = TraderUpdateKind::try_from(
                        param.value.into_uint().unwrap().low_u32() as u8,
                    )?;
                }
                _ => bail!("Unexpected param for TraderUpdate {:?}", param),
            }
        }
        event.tx_stamp = Some(BlockTxStamp {
            block_number: 0,
            tx_hash: log.tx_hash.into(),
        });
        Ok(event)
    }
}

impl ParseLog for CheckpointConfirmed {
    fn from_log(log: LogEntry) -> Result<Self> {
        let raw_log = RawLog {
            topics: log.topics.clone(),
            data: log.data,
        };

        let log_event = CheckpointedEvent::default();
        let log_ = parse_event_log(log_event.0, raw_log)?;
        let mut event = CheckpointConfirmed::default();
        for param in log_.params {
            // It's safe to unwrap here because we know the rules by construction
            match param.name.as_str() {
                "stateRoot" => {
                    event.state_root =
                        Bytes32::from_slice(&param.value.into_fixed_bytes().unwrap()).into()
                }
                "transactionRoot" => {
                    event.tx_root =
                        Bytes32::from_slice(&param.value.into_fixed_bytes().unwrap()).into()
                }
                "epochId" => event.epoch_id = param.value.into_uint().unwrap().low_u64(),
                "custodians" => {
                    event.custodians = param
                        .value
                        .into_array()
                        .unwrap()
                        .into_iter()
                        .map(|a| a.into_address().unwrap().into())
                        .collect()
                }
                "bonds" => {
                    event.bonds = param
                        .value
                        .into_array()
                        .unwrap()
                        .into_iter()
                        .map(|b| {
                            (U128::from(b.into_uint().unwrap().low_u128())
                                / U128::from_dec_str("1000000000000").unwrap())
                            .into()
                        })
                        .collect()
                }
                "submitter" => event.submitter = param.value.into_address().unwrap().into(),
                _ => bail!("Unexpected param {:?}", param),
            }
        }
        event.tx_stamp = Some(BlockTxStamp {
            block_number: Default::default(),
            tx_hash: log.tx_hash.into(),
        });
        Ok(event)
    }
}

impl ParseLog for InsuranceFundUpdate<RecordedAmount> {
    fn from_log(log: LogEntry) -> Result<Self> {
        // Web3/ethabi gyrations to parse the event into a structured log
        let raw_log = RawLog {
            topics: log.topics.clone(),
            data: log.data,
        };
        let insurance_event = InsuranceFundUpdatedEvent::default();
        let log_ = parse_event_log(insurance_event.0, raw_log)?;
        let mut event = InsuranceFundUpdate::default();
        for param in log_.params {
            // It's safe to unwrap here because we know the rules by construction
            match param.name.as_str() {
                "contributor" => {
                    event.address =
                        InsuranceFundContributorAddress(param.value.into_address().unwrap().into())
                }
                "collateralAddress" => {
                    event.collateral_address =
                        TokenAddress::collateral(param.value.into_address().unwrap())
                }
                "amount" => {
                    event.amount = U128::try_from(param.value.into_uint().unwrap())
                        .unwrap()
                        .into()
                }
                "updateKind" => {
                    event.update_kind = InsuranceFundUpdateKind::try_from(
                        param.value.into_uint().unwrap().low_u32() as u8,
                    )?
                }
                _ => bail!("Unexpected param for InsuranceFundUpdate {:?}", param),
            }
        }
        event.tx_hash = log.tx_hash.into();
        Ok(event)
    }
}

#[derive(Debug, Default, Clone, PartialEq, Deserialize, Serialize, AbiToken)]
#[serde(rename_all = "camelCase")]
pub struct SignerRegisteredMeta {
    pub release_hash: ReleaseHash,
    pub custodian: TraderAddress,
    pub signer_address: SignerAddress,
    pub tx_hash: Hash,
}

impl ParseLog for SignerRegisteredMeta {
    fn from_log(log: LogEntry) -> Result<Self> {
        // Web3/ethabi gyrations to parse the event into a structured log
        let raw_log = RawLog {
            topics: log.topics.clone(),
            data: log.data,
        };
        let signer_registered_event = SignerRegisteredEvent::default();
        let log_ = parse_event_log(signer_registered_event.0, raw_log)?;
        let mut event = SignerRegisteredMeta::default();
        for param in log_.params {
            // It's safe to unwrap here because we know the rules by construction
            match param.name.as_str() {
                "releaseHash" => {
                    event.release_hash = Bytes32::from_slice(
                        &param
                            .value
                            .into_fixed_bytes()
                            .ok_or_else(|| error!("invalid releaseHash"))?,
                    )
                    .into()
                }
                "custodian" => {
                    event.custodian = param
                        .value
                        .into_address()
                        .ok_or_else(|| error!("invalid custodian"))?
                        .into()
                }
                "signer" => {
                    event.signer_address = param
                        .value
                        .into_address()
                        .ok_or_else(|| error!("invalid signer"))?
                        .into()
                }
                _ => bail!("Unexpected param for SignerRegistered {:?}", param),
            }
        }
        event.tx_hash = log.tx_hash.into();
        Ok(event)
    }
}

#[derive(Debug, Clone, Copy, Default, Deserialize, Serialize, PartialEq)]
#[serde(rename_all = "camelCase")]
pub struct ReleaseUpdate {
    pub release_hash: ReleaseHash,
    pub starting_epoch_id: EpochId,
}

impl ParseLog for ReleaseUpdate {
    fn from_log(log: LogEntry) -> Result<Self> {
        // Web3/ethabi gyrations to parse the event into a structured log
        let raw_log = RawLog {
            topics: log.topics.clone(),
            data: log.data,
        };
        let release_schedule_updated_event = ReleaseScheduleUpdatedEvent::default();
        let log_ = parse_event_log(release_schedule_updated_event.0, raw_log)?;
        let mut mr_enclave: Bytes32 = Default::default();
        let mut isvsvn: u16 = Default::default();
        let mut event = ReleaseUpdate::default();
        for param in log_.params {
            // It's safe to unwrap here because we know the rules by construction
            match param.name.as_str() {
                "mrEnclave" => {
                    mr_enclave = Bytes32::from_slice(
                        &param
                            .value
                            .into_fixed_bytes()
                            .ok_or_else(|| error!("invalid mrEnclave"))?,
                    );
                }
                "isvSvn" => {
                    isvsvn = u16::from_be_bytes(
                        param
                            .value
                            .into_fixed_bytes()
                            .ok_or_else(|| error!("invalid isvsvn"))?
                            .try_into()
                            .map_err(|_| error!("Failed to convert isvsvn bytes into u16"))?,
                    );
                }
                "startingEpochId" => {
                    event.starting_epoch_id = param.value.into_uint().unwrap().low_u64();
                }
                _ => panic!("Unexpected param for ReleaseScheduleUpdated {:?}", param),
            }
        }
        event.release_hash = ReleaseHash::new(mr_enclave.as_bytes(), isvsvn);
        tracing::debug!(?event, "Parsed ReleaseUpdate event");
        Ok(event)
    }
}
