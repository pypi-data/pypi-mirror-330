use chrono::{DateTime, Utc};
use ethereum_types::{Address, H520, U256};
use rust_decimal::Decimal;
use serde::{Deserialize, Serialize};
use std::time::Duration;

use crate::{
    Result,
    crypto::Keccak256,
    global::Chain,
    impl_signing,
    types::primitives::{Hash, OrderSide, UnscaledI128},
    util::eip712::{HashEIP712, Message, Payload},
};

use super::{SessionNotice, Symbol, ValueError, strategy::StrategyId};

/// The kind of action that was taken in the execution report.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize, Default)]
pub enum ExecutionKind {
    New,
    Replaced,
    Canceled,
    #[default]
    Fill,
    Rejected,
    Expired,
}

impl TryFrom<char> for ExecutionKind {
    type Error = ValueError;

    fn try_from(value: char) -> Result<Self, Self::Error> {
        match value {
            '0' => Ok(ExecutionKind::New),
            '4' => Ok(ExecutionKind::Canceled),
            '5' => Ok(ExecutionKind::Replaced),
            '8' => Ok(ExecutionKind::Rejected),
            'F' => Ok(ExecutionKind::Fill),
            'C' => Ok(ExecutionKind::Expired),
            _ => Err(ValueError::ParsingError {
                error: format!("Invalid execution kind: {}", value),
            }),
        }
    }
}

impl From<ExecutionKind> for char {
    fn from(val: ExecutionKind) -> Self {
        match val {
            ExecutionKind::New => '0',
            ExecutionKind::Fill => 'F',
            ExecutionKind::Canceled => '4',
            ExecutionKind::Rejected => '8',
            ExecutionKind::Expired => 'C',
            ExecutionKind::Replaced => '5',
        }
    }
}

impl From<ExecutionKind> for u8 {
    fn from(val: ExecutionKind) -> Self {
        let c: char = val.into();
        c.to_ascii_uppercase() as u8
    }
}

/// Order statuses as defined by the FIX protocol.
///
/// https://docs.cdp.coinbase.com/intx/docs/fix-msg-drop-copy#executionreport-358
/// 0 - NEW
/// 1 - PARTIALLY_FILLED
/// 2 - FILLED
/// 4 - CANCELED
/// 6 - PENDING_CANCEL
/// 8 - REJECTED
/// A - PENDING_NEW
/// E - PENDING_REPLACE
/// C - EXPIRED
/// Status of an order, this can typically change over time
#[derive(Debug, Serialize, Deserialize, Clone, PartialEq, Eq)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
#[derive(Default)]
pub enum OrderStatus {
    /// The order has been accepted by the engine.
    New,
    /// A part of the order has been filled.
    PartiallyFilled,
    /// The order has been completely filled.
    #[default]
    Filled,
    /// The order has been canceled by the user.
    Canceled,
    /// (currently unused)
    PendingCancel,
    /// Used by Coinbase
    PendingNew,
    /// Used by Coinbase
    PendingReplace,
    /// The order was not accepted by the engine and not processed.
    Rejected,
    /// The order was canceled according to the order type's rules (e.g. LIMIT FOK orders with no fill, LIMIT IOC or MARKET orders that partially fill) or by the exchange, (e.g. orders canceled during liquidation, orders canceled during maintenance)
    Expired,
}

impl TryFrom<char> for OrderStatus {
    type Error = ValueError;

    fn try_from(c: char) -> Result<Self, Self::Error> {
        match c {
            '0' => Ok(OrderStatus::New),
            '1' => Ok(OrderStatus::PartiallyFilled),
            '2' => Ok(OrderStatus::Filled),
            '4' => Ok(OrderStatus::Canceled),
            '6' => Ok(OrderStatus::PendingCancel),
            '8' => Ok(OrderStatus::Rejected),
            'A' => Ok(OrderStatus::PendingNew),
            'C' => Ok(OrderStatus::Expired),
            'E' => Ok(OrderStatus::PendingReplace),
            _ => Err(ValueError::ParsingError {
                error: format!("Invalid order status: {}", c),
            }),
        }
    }
}

impl From<OrderStatus> for char {
    fn from(val: OrderStatus) -> Self {
        match val {
            OrderStatus::New => '0',
            OrderStatus::PartiallyFilled => '1',
            OrderStatus::Filled => '2',
            OrderStatus::Canceled => '4',
            OrderStatus::PendingCancel => '6',
            OrderStatus::PendingNew => 'A',
            OrderStatus::PendingReplace => 'E',
            OrderStatus::Rejected => '8',
            OrderStatus::Expired => 'C',
        }
    }
}

/// Convert an OrderStatus to a u8.
/// The ASCII value of the uppercase character is returned.
impl From<OrderStatus> for u8 {
    fn from(val: OrderStatus) -> Self {
        let c: char = val.into();
        c.to_ascii_lowercase() as u8
    }
}

/// Order types as defined by the FIX protocol.
///
/// https://developers.binance.com/docs/binance-spot-api-docs/testnet/fix-api#executionreport8
/// Possible values:
/// 1 - MARKET
/// 2 - LIMIT
/// 3 - STOP_LOSS
/// 4 - STOP_LIMIT
#[derive(Debug, Serialize, Deserialize, Clone, PartialEq, Eq)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
#[derive(Default)]
pub enum OrderType {
    Limit,
    #[default]
    Market,
    StopLoss,
    StopLimit,
    #[serde(other)]
    Other,
}

impl From<char> for OrderType {
    fn from(value: char) -> Self {
        match value {
            '1' => OrderType::Market,
            '2' => OrderType::Limit,
            '3' => OrderType::StopLoss,
            '4' => OrderType::StopLimit,
            _ => OrderType::Other,
        }
    }
}

impl From<OrderType> for char {
    fn from(val: OrderType) -> Self {
        match val {
            OrderType::Limit => '2',
            OrderType::Market => '1',
            OrderType::StopLoss => '3',
            OrderType::StopLimit => '4',
            OrderType::Other => '0',
        }
    }
}

impl From<OrderType> for u8 {
    fn from(val: OrderType) -> Self {
        let c: char = val.into();
        c.to_ascii_lowercase() as u8
    }
}

/// Final message to be streamed to copy-traders after each execution.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "camelCase")]
pub struct ExecutionAnnouncement {
    /// Public identifier for the leader, includes the Ethereum address.
    pub strategy_id: StrategyId,
    /// The kind of execution (e.g., new, modify, cancel).
    pub kind: ExecutionKind,
    /// Symbol of the market (e.g., BTCUSDT).
    pub symbol: Symbol,
    /// Order quantity as a percentage of a $10,000 portfolio
    /// (following the eToro-like relative portfolio value approach).
    /// TODO: This requires a notion of approximate or relative value of the quote currency.
    pub size_percent: UnscaledI128,
    /// The side of the order (buy/sell).
    pub side: OrderSide,
    /// The type of order (e.g., limit, market).
    pub ord_type: OrderType,
    /// Price at which the order was placed.
    pub price: UnscaledI128,
    /// Time of the transaction.
    pub transact_time: i64,
    /// Percentage remaining unfilled relative to the original OrderQty.
    pub unfilled_percent: UnscaledI128,
    /// Price of the last execution, if applicable.
    pub last_px: Option<UnscaledI128>,
    /// Quantity of the last execution, if applicable.
    pub last_qty: Option<UnscaledI128>,
    /// Status of the order (e.g., filled, partially filled, canceled).
    pub ord_status: OrderStatus,
    /// EIP-191 signature of this message by the enclave's signing key.
    pub signature: H520,
    #[cfg(feature = "test_harness")]
    pub order_id: u64,
}

impl ExecutionAnnouncement {
    /// Create an unsigned execution announcement from an execution report.
    pub fn from_execution_report(
        strategy_id: StrategyId,
        execution: &ExecutionReportMessage,
    ) -> Self {
        // Calculate unfilled percentage
        let unfilled_percent = if execution.order_qty != Decimal::ZERO {
            execution.leaves_qty / execution.order_qty * Decimal::from(100)
        } else {
            Decimal::ZERO
        };

        ExecutionAnnouncement {
            strategy_id,
            kind: execution.exec_type.clone(),
            symbol: execution.symbol.clone(),
            size_percent: UnscaledI128::ZERO, // TODO: Implement calculation based on portfolio value
            side: execution.side,
            ord_type: execution.ord_type.clone(),
            price: execution.price.into(),
            transact_time: execution.transact_time.timestamp(),
            unfilled_percent: unfilled_percent.into(),
            last_px: execution.last_px.map(|p| p.into()),
            last_qty: execution.last_qty.map(|q| q.into()),
            ord_status: execution.ord_status.clone(),
            signature: Default::default(),
            #[cfg(feature = "test_harness")]
            order_id: execution.order_id,
        }
    }

    /// Serialize the announcement into a byte vector
    pub fn serialize(&self) -> Result<Vec<u8>, ValueError> {
        serde_json::to_vec(self).map_err(|e| ValueError::SerializationError {
            error: e.to_string(),
        })
    }

    pub fn deserialize(bytes: &[u8]) -> Result<Self, ValueError> {
        serde_json::from_slice(bytes).map_err(|e| ValueError::SerializationError {
            error: e.to_string(),
        })
    }
}

impl_signing!(ExecutionAnnouncement);

impl HashEIP712 for ExecutionAnnouncement {
    fn hash_eip712_raw(&self, chain: Chain, contract_address: Address) -> Result<Hash> {
        let mut message = Message::new(chain, contract_address)?;
        let mut payload = Payload::from_signature(
            b"ExecutionAnnouncement(bytes32 strategyId,uint256 kind,bytes32 symbol,uint256 sizePercent,uint256 side,uint256 ordType,uint256 price,uint256 transactTime,uint256 unfilledPercent,uint256 lastPx,uint256 lastQty,uint256 ordStatus)".to_vec(),
        );
        payload.append(self.strategy_id.keccak256());
        let kind: u8 = self.kind.clone().into();
        payload.append(U256::from(kind));
        payload.append(self.symbol.keccak256());
        payload.append(U256::from(self.size_percent));
        let side: u8 = self.side.into();
        payload.append(U256::from(side));
        let ord_type: u8 = self.ord_type.clone().into();
        payload.append(U256::from(ord_type));
        payload.append(U256::from(self.price));
        payload.append(U256::from(self.transact_time));
        payload.append(U256::from(self.unfilled_percent));
        payload.append(U256::from(self.last_px.unwrap_or(UnscaledI128::ZERO)));
        payload.append(U256::from(self.last_qty.unwrap_or(UnscaledI128::ZERO)));
        let ord_status: u8 = self.ord_status.clone().into();
        payload.append(U256::from(ord_status));
        message.append_payload(payload);
        Ok(message.finalize())
    }
}

/// Represents a decoded Execution Report message.
#[derive(Debug, Default)]
pub struct ExecutionReportMessage {
    /// Type in alignment with the Binance crate
    pub order_id: u64,
    pub symbol: Symbol,
    pub order_qty: Decimal,
    pub side: OrderSide,
    pub ord_type: OrderType,
    pub price: Decimal,
    pub transact_time: DateTime<Utc>,
    pub exec_type: ExecutionKind,
    pub cum_qty: Decimal,
    pub leaves_qty: Decimal,
    pub trade_id: Option<String>,
    pub last_px: Option<Decimal>,
    pub last_qty: Option<Decimal>,
    pub ord_status: OrderStatus,
}

/// Represents an execution announcement or administrative message for a specific strategy.
///
/// This is the data type used for messages in the public FOLLOWER STREAM.
// TODO: Align with SessionStatus for consistency and sufficient health monitoring.
#[derive(Debug, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "camelCase")]
#[serde(tag = "type")]
#[allow(clippy::large_enum_variant)]
pub enum StrategyEvent<E> {
    /// Indicates the subaccount's FIX session is online and actively responding to heartbeats.
    /// Includes duration since last Logon acknowledgement.
    Online(Duration),
    /// Indicates the subaccount's FIX session is offline, logged out, and unable to reconnect.
    /// Includes duration since last logout or disconnection.
    Offline(Duration),
    /// A user-facing notice requiring action.
    SessionNotice { notice: SessionNotice },
    /// Execution announcement encrypted or unencrypted.
    ExecutionAnnouncement { announcement: E },
    /// Strategy checkpoint update.
    StrategyCheckpoint { checkpoint: StrategyCheckpoint },
}

impl From<StrategyEvent<ExecutionAnnouncement>> for StrategyEvent<String> {
    fn from(event: StrategyEvent<ExecutionAnnouncement>) -> Self {
        match event {
            StrategyEvent::ExecutionAnnouncement { announcement: _ } => {
                panic!("ExecutionAnnouncement cannot be implicitly converted to String");
            }
            StrategyEvent::Online(duration) => StrategyEvent::Online(duration),
            StrategyEvent::Offline(duration) => StrategyEvent::Offline(duration),
            StrategyEvent::SessionNotice { notice } => StrategyEvent::SessionNotice { notice },
            StrategyEvent::StrategyCheckpoint { checkpoint } => {
                StrategyEvent::StrategyCheckpoint { checkpoint }
            }
        }
    }
}

/// A delayed allocation.
#[derive(Debug, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "camelCase")]
pub struct Allocation {
    pub symbol: Symbol,
    pub qty: Decimal,
}

/// A strategy checkpoint, also serves as a strategy status update to indicate
/// the aliveness of the strategy.
#[derive(Debug, Default, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "camelCase")]
pub struct StrategyCheckpoint {
    /// The current realized PnL (in USD).
    pub pnl: Decimal,
    /// The portfolio allocation at the time of the checkpoint.
    pub allocations: Vec<Allocation>,
    /// Timestamp of the checkpoint.
    pub timestamp: DateTime<Utc>,
}

impl StrategyCheckpoint {
    pub fn new(pnl: Decimal, allocation: Vec<Allocation>) -> Self {
        Self {
            pnl,
            allocations: allocation,
            timestamp: Utc::now(),
        }
    }
}

/// The public type of the strategy event with the strategy id as an optional field.
/// If the event has no strategy id, it is a public event.
#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct StrategyEventWithId<E> {
    pub strategy_id: StrategyId,
    pub event: StrategyEvent<E>,
}

#[cfg(test)]
mod tests {
    use base64::Engine;

    use super::*;

    #[test]
    fn test_serialize_execution_announcement() {
        let announcement = ExecutionAnnouncement::from_execution_report(
            StrategyId::default(),
            &ExecutionReportMessage::default(),
        );
        let serialized = announcement.clone().serialize().unwrap();
        // not encrypted in this test
        let encoded = base64::engine::general_purpose::STANDARD.encode(&serialized);
        let strategy_event = StrategyEvent::ExecutionAnnouncement {
            announcement: encoded,
        };
        let serialized = serde_json::to_string(&strategy_event).unwrap();
        println!("serialized: {}", serialized);
        let deserialized: StrategyEvent<String> = serde_json::from_str(&serialized).unwrap();
        if let StrategyEvent::ExecutionAnnouncement {
            announcement: decoded,
        } = deserialized
        {
            let decoded = base64::engine::general_purpose::STANDARD
                .decode(&decoded)
                .unwrap();
            let deserialized: ExecutionAnnouncement = serde_json::from_slice(&decoded).unwrap();
            assert_eq!(announcement, deserialized);
        } else {
            panic!("Deserialized event is not an encrypted execution announcement");
        }
    }

    #[test]
    fn test_serialize_session_notice_event() {
        // test serialization of a SessionNotice
        let notice = SessionNotice::AuthenticationError {
            error: "This is a test notice".to_string(),
        };
        let event = StrategyEvent::<String>::SessionNotice { notice };
        let serialized = serde_json::to_string(&event).unwrap();
        println!("serialized: {}", serialized);
        let deserialized: StrategyEvent<String> = serde_json::from_str(&serialized).unwrap();
        assert_eq!(event, deserialized);

        // test serialization of a ValueError
        let value_error = ValueError::SerializationError {
            error: "This is a test notice".to_string(),
        };
        let notice = SessionNotice::ValueError(value_error);
        let event = StrategyEvent::<String>::SessionNotice { notice };
        let serialized = serde_json::to_string(&event).unwrap();
        println!("serialized: {}", serialized);
        let deserialized: StrategyEvent<String> = serde_json::from_str(&serialized).unwrap();
        assert_eq!(event, deserialized);
    }

    #[test]
    fn test_serialize_strategy_checkpoint_event() {
        let checkpoint = StrategyCheckpoint {
            pnl: Decimal::from(100),
            allocations: vec![Allocation {
                symbol: Symbol::new("BTC"),
                qty: Decimal::from(100),
            }],
            timestamp: Utc::now(),
        };
        let event = StrategyEvent::<String>::StrategyCheckpoint { checkpoint };
        let serialized = serde_json::to_string(&event).unwrap();
        println!("serialized: {}", serialized);
        let deserialized: StrategyEvent<String> = serde_json::from_str(&serialized).unwrap();
        assert_eq!(event, deserialized);
    }
}
