#[cfg(feature = "python")]
use crate::types::state::exported;
use ddx_common_macros::{AbiToken, dec};
use lazy_static::lazy_static;
#[cfg(feature = "database")]
use postgres_types::{FromSql, IsNull, ToSql, Type, to_sql_checked};
#[cfg(feature = "python")]
use pyo3::prelude::*;
#[cfg(feature = "arbitrary")]
use quickcheck::Arbitrary;
use rust_decimal::{
    Decimal,
    prelude::{FromPrimitive, One, Zero},
};
use serde::{Deserialize, Serialize};
use std::{
    collections::HashMap,
    convert::{TryFrom, TryInto},
    fmt::{self, Debug, Formatter},
    ops::Neg,
    str::FromStr,
};

use crate::{
    Error, Result, bail,
    ethabi::Token,
    specs::constants::{FUNDING_LOWER_BOUND, FUNDING_UPPER_BOUND},
    types::{
        primitives::{
            Bytes32, FixedBytesWrapper, OrderSide, ProductSymbol, TimeValue, TokenSymbol,
            UnscaledI128,
        },
        state::VoidableItem,
    },
    util::{
        serde::{as_bytes32_text, as_scaled_fraction},
        tokenize::Tokenizable,
    },
};

#[cfg(feature = "index_fund")]
use crate::types::primitives::UnderlyingSymbol;
#[cfg(feature = "index_fund")]
use std::collections::BTreeMap;

mod balance;
pub use balance::Balance;

pub const MAIN_STRAT: &str = "main";
pub const DEFAULT_MAX_LEVERAGE: u64 = 3;

lazy_static! {
    static ref EMA_PERIODS: Decimal = Decimal::from(30);
    pub static ref MAKER_FEE_BPS: Decimal = Decimal::from_f32(0.0).unwrap();
    // The taker fee is currently set to 20 bps
    pub static ref TAKER_FEE_BPS: Decimal = Decimal::from_f32(0.002).unwrap();
    // The maintenance margin fraction. A maintenance margin fraction of
    // 0.15 gives a maintenance margin ratio of 0.15 / 3 = 0.05.
    pub static ref MMR_FRACTION: Decimal = Decimal::from_f32(0.15).unwrap();
}

/// Bare minimum `Strategy` data required by common accounting ops
#[derive(Debug, Default, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct StrategyMetrics {
    pub margin: UnscaledI128,
    pub max_leverage: u64,
    pub positions: HashMap<ProductSymbol, Position>,
}

impl StrategyMetrics {
    #[cfg(test)]
    pub fn new(
        margin: Decimal,
        max_leverage: u64,
        positions: HashMap<ProductSymbol, Position>,
    ) -> Self {
        StrategyMetrics {
            margin: margin.into(),
            max_leverage,
            positions,
        }
    }

    pub fn from_strategy(strategy: &Strategy, positions: HashMap<ProductSymbol, Position>) -> Self {
        StrategyMetrics {
            margin: strategy.avail_collateral.get_or_default(TokenSymbol::USDC),
            max_leverage: strategy.max_leverage,
            positions,
        }
    }

    pub fn symbols(&self) -> Vec<ProductSymbol> {
        let mut symbols = self.positions.keys().copied().collect::<Vec<_>>();
        symbols.sort();
        symbols
    }
}

/// An trading strategy (aka sub-account, formerly known as account)
#[cfg_attr(feature = "python", pyclass(get_all, set_all))]
#[derive(Debug, Clone, PartialEq, Deserialize, Serialize, AbiToken, Eq)]
#[serde(rename_all = "camelCase")]
#[repr(C)]
pub struct Strategy {
    /// Amount of the collateral per token available as margin
    pub avail_collateral: Balance,
    /// Amount of collateral per token frozen for withdrawal
    pub locked_collateral: Balance,
    /// Maximum amount of leverage allowed
    pub max_leverage: u64,
    /// Whether the entire account frozen for strategy tokenization
    pub frozen: bool,
}

impl VoidableItem for Strategy {
    fn is_void(&self) -> bool {
        self.avail_collateral.is_void() && self.locked_collateral.is_void()
    }
}

#[cfg(feature = "python")]
#[pymethods]
impl Strategy {
    #[new]
    pub(crate) fn new_py() -> Self {
        Self {
            avail_collateral: Default::default(),
            locked_collateral: Default::default(),
            max_leverage: DEFAULT_MAX_LEVERAGE,
            frozen: false,
        }
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for Strategy {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        Self {
            avail_collateral: Balance::arbitrary(g),
            locked_collateral: Balance::arbitrary(g),
            max_leverage: u64::arbitrary(g),
            frozen: bool::arbitrary(g),
        }
    }
}

impl Default for Strategy {
    fn default() -> Self {
        Strategy {
            avail_collateral: Balance::default(),
            locked_collateral: Balance::default(),
            max_leverage: DEFAULT_MAX_LEVERAGE,
            frozen: false,
        }
    }
}

impl Strategy {
    pub fn new() -> Strategy {
        Strategy {
            avail_collateral: Default::default(),
            locked_collateral: Default::default(),
            max_leverage: DEFAULT_MAX_LEVERAGE,
            frozen: false,
        }
    }

    #[cfg(feature = "test_harness")]
    pub fn default_with_collateral(collateral: Balance) -> Strategy {
        // convert the collateral to margin
        Strategy {
            avail_collateral: Balance::new(collateral[TokenSymbol::USDC], TokenSymbol::USDC),
            locked_collateral: Default::default(),
            max_leverage: DEFAULT_MAX_LEVERAGE,
            frozen: false,
        }
    }
}

#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, std::hash::Hash, Deserialize, Serialize)]
pub struct StrategyId(#[serde(with = "as_bytes32_text")] pub Bytes32);

#[cfg(feature = "python")]
impl FromPyObject<'_> for StrategyId {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let string: String = ob.extract()?;
        Ok(StrategyId::from_string(string)?)
    }
}

#[cfg(feature = "python")]
impl IntoPy<PyObject> for StrategyId {
    fn into_py(self, py: Python) -> PyObject {
        self.0.to_string().into_py(py)
    }
}

impl fmt::Display for StrategyId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl StrategyId {
    fn new(value: Bytes32) -> Self {
        // First validate that the bytes 32 value is valid utf8
        // If not, default to using the main strategy
        let val_bytes = value.as_bytes();
        let str_len = val_bytes[0];

        if str_len > 31 {
            tracing::warn!("Length of Bytes32 can't be greater than 31");
            return StrategyId::from_string(MAIN_STRAT.to_string()).unwrap();
        }

        let str_bytes = &val_bytes[1..str_len as usize + 1];
        if let Err(e) = std::str::from_utf8(str_bytes) {
            tracing::warn!(
                ?e,
                "Strategy Id bytes were not valid, using default strategy instead"
            );
            StrategyId::from_string(MAIN_STRAT.to_string()).unwrap()
        } else {
            StrategyId(value)
        }
    }
    // This constructor is used to enforce regularity conditions on the contents
    // of StrategyIds that ensures that every StrategyId can be abi-encoded as a
    // Bytes32 value.
    pub fn from_string(string: String) -> Result<Self> {
        let id = Bytes32::from_str(&string)?;
        Ok(StrategyId(id))
    }
}

impl Tokenizable for StrategyId {
    fn from_token(token: Token) -> Result<Self>
    where
        Self: Sized,
    {
        let token_bytes32: Bytes32 = Bytes32::from_token(token)?;
        Ok(StrategyId(token_bytes32))
    }

    fn into_token(self) -> Token {
        // We can unwrap here because every StrategyId is shorter than 32 bytes
        self.0.into_token()
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for StrategyId {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        let size: i32 = *g.choose(&(0..32 / 4).collect::<Vec<i32>>()).unwrap();
        let strategy = (0..size).map(|_| char::arbitrary(g)).collect();
        Self::from_string(strategy).unwrap()
    }
}

impl Default for StrategyId {
    fn default() -> Self {
        StrategyId::from_string(MAIN_STRAT.to_string()).unwrap()
    }
}

#[cfg(feature = "test_harness")]
impl From<&str> for StrategyId {
    fn from(val: &str) -> Self {
        StrategyId(Bytes32::from_str(val).unwrap())
    }
}

impl TryFrom<StrategyId> for Bytes32 {
    type Error = Error;

    fn try_from(value: StrategyId) -> Result<Self, Self::Error> {
        Ok(value.0)
    }
}

impl From<Bytes32> for StrategyId {
    fn from(value: Bytes32) -> Self {
        StrategyId::new(value)
    }
}

impl fmt::Debug for StrategyId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_tuple("StrategyId")
            .field(&self.0.to_string())
            .finish()
    }
}

#[cfg(feature = "database")]
impl ToSql for StrategyId {
    fn to_sql(
        &self,
        ty: &Type,
        out: &mut bytes::BytesMut,
    ) -> Result<IsNull, Box<dyn std::error::Error + 'static + Sync + Send>> {
        self.0.to_string().to_sql(ty, out)
    }

    fn accepts(ty: &Type) -> bool {
        <String as ToSql>::accepts(ty)
    }

    to_sql_checked!();
}

#[cfg(feature = "database")]
impl<'a> FromSql<'a> for StrategyId {
    fn from_sql(
        ty: &Type,
        raw: &'a [u8],
    ) -> Result<Self, Box<dyn std::error::Error + Sync + Send>> {
        let decoded_string: String = String::from_sql(ty, raw)?;
        let strategy_id: StrategyId = Self::from_string(decoded_string)?;
        Ok(strategy_id)
    }

    fn accepts(ty: &Type) -> bool {
        <String as FromSql>::accepts(ty)
    }
}

#[cfg_eval]
#[cfg_attr(feature = "python", pyclass(frozen))]
#[derive(
    Debug,
    Copy,
    Clone,
    Hash,
    PartialEq,
    Deserialize,
    Serialize,
    AbiToken,
    Eq,
    PartialOrd,
    Ord,
    Default,
)]
pub enum PositionSide {
    #[cfg_attr(feature = "python", pyo3(name = "Empty"))]
    #[default]
    None,
    Long,
    Short,
}

impl PositionSide {
    #[tracing::instrument(level = "trace")]
    pub fn avg_pnl(&self, avg_entry_price: Decimal, ref_price: Decimal) -> Decimal {
        match self {
            PositionSide::Long => ref_price - avg_entry_price,
            PositionSide::Short => avg_entry_price - ref_price,
            PositionSide::None => Decimal::zero(),
        }
    }

    #[tracing::instrument(level = "trace")]
    pub(crate) fn unrealized_pnl(
        &self,
        avg_entry_price: Decimal,
        ref_price: Decimal,
        balance: Decimal,
    ) -> Decimal {
        self.avg_pnl(avg_entry_price, ref_price) * balance
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for PositionSide {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        let discriminator = *g.choose(&[0, 1, 2]).unwrap();
        match discriminator {
            0 => PositionSide::None,
            1 => PositionSide::Long,
            2 => PositionSide::Short,
            _ => panic!("invalid  discriminator"),
        }
    }
}

// TODO: Standardize the discriminant conversion of all enums
// All short enums codes are u8 to ensure that we can use only 1 byte in binary encoding
impl From<PositionSide> for u8 {
    fn from(value: PositionSide) -> Self {
        match value {
            PositionSide::None => 0,
            PositionSide::Long => 1,
            PositionSide::Short => 2,
        }
    }
}

impl TryFrom<u8> for PositionSide {
    type Error = Error;

    fn try_from(value: u8) -> Result<Self, Self::Error> {
        Ok(match value {
            0 => PositionSide::None,
            1 => PositionSide::Long,
            2 => PositionSide::Short,
            _ => bail!("Invalid position side code {:?}", value),
        })
    }
}

impl TryFrom<i32> for PositionSide {
    type Error = Error;

    fn try_from(value: i32) -> Result<Self, Self::Error> {
        let byte: u8 = u8::try_from(value)?;
        let result: Self = Self::try_from(byte)?;
        Ok(result)
    }
}

impl TryInto<OrderSide> for PositionSide {
    type Error = Error;

    fn try_into(self) -> Result<OrderSide, Self::Error> {
        Ok(match self {
            PositionSide::Short => OrderSide::Ask,
            PositionSide::Long => OrderSide::Bid,
            PositionSide::None => bail!("An empty position has no side"),
        })
    }
}

#[cfg(feature = "database")]
impl ToSql for PositionSide {
    fn to_sql(
        &self,
        ty: &Type,
        out: &mut bytes::BytesMut,
    ) -> Result<IsNull, Box<dyn std::error::Error + 'static + Sync + Send>> {
        let value: i32 = (*self as u8).into();
        value.to_sql(ty, out)
    }

    fn accepts(ty: &Type) -> bool {
        <i32 as ToSql>::accepts(ty)
    }

    to_sql_checked!();
}

#[cfg(feature = "database")]
impl<'a> FromSql<'a> for PositionSide {
    fn from_sql(
        ty: &Type,
        raw: &'a [u8],
    ) -> Result<Self, Box<dyn std::error::Error + Sync + Send>> {
        let decoded: i32 = i32::from_sql(ty, raw)?;
        let result: Self = Self::try_from(decoded)?;
        Ok(result)
    }

    fn accepts(ty: &Type) -> bool {
        <i32 as FromSql>::accepts(ty)
    }
}

/// An individual position held in an strategy
#[cfg_attr(feature = "python", pyclass(get_all, set_all))]
#[derive(Clone, Debug, Default, PartialEq, Eq, Deserialize, Serialize, AbiToken)]
#[serde(rename_all = "camelCase")]
#[repr(C)]
pub struct Position {
    /// The position side: Long = 0, Short = 1
    pub side: PositionSide,
    /// The position size denominated in the same unit as the underlying
    pub balance: UnscaledI128,
    /// The average entry price (updated when adding to the position)
    pub avg_entry_price: UnscaledI128,
}

#[cfg(feature = "python")]
#[pymethods]
impl Position {
    #[new]
    fn new_py(side: PositionSide, balance: UnscaledI128, avg_entry_price: UnscaledI128) -> Self {
        Self {
            side,
            balance,
            avg_entry_price,
        }
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for Position {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        Self {
            side: PositionSide::arbitrary(g),
            balance: Arbitrary::arbitrary(g),
            avg_entry_price: Arbitrary::arbitrary(g),
        }
    }
}

impl VoidableItem for Position {
    fn is_void(&self) -> bool {
        self.balance.is_zero()
    }
}

impl Position {
    pub fn bankruptcy_price(&self, mark_price: Decimal, account_total_value: Decimal) -> Decimal {
        // ```python
        // side = Decimal("1") if self.side == PositionSide.LONG else Decimal("-1")
        // return price.mark_price() - side * (total_value / self.balance)
        // ````
        let side_mul = match self.side {
            PositionSide::Long => Decimal::one(),
            PositionSide::Short => Decimal::one().neg(),
            PositionSide::None => panic!("Bankruptcy price not applicable to empty position"),
        };

        mark_price - side_mul * (account_total_value / *self.balance)
    }

    /// Calculate the unrealized pnl using the current balance
    pub fn unrealized_pnl(&self, price: Decimal) -> Decimal {
        self.side
            .unrealized_pnl(self.avg_entry_price.into(), price, self.balance.into())
    }

    /// Calculate the avg pnl, avg entry price relative to price reference
    pub fn avg_pnl(&self, price: Decimal) -> Decimal {
        self.side.avg_pnl(*self.avg_entry_price, price)
    }

    #[cfg(not(target_family = "wasm"))]
    pub(crate) fn increase(&mut self, price: Decimal, amount: Decimal) -> Decimal {
        // Adjusting the average entry price
        let avg_entry_price = match self.side {
            PositionSide::None => price,
            _ => self.calculate_avg_entry_price(price, amount),
        };
        self.avg_entry_price = avg_entry_price.into();
        // Adding the fill to the existing balance
        let balance = *self.balance + amount;
        self.balance = balance.into();
        // The pnl is always 0 because we're not closing any trades
        Decimal::zero()
    }

    pub fn decrease(&mut self, price: Decimal, amount: Decimal) -> Decimal {
        // The pnl is based on the fill amount because we're decreasing it
        let pnl = amount * self.avg_pnl(price);
        // Subtracting the amount from the balance to decrease the position
        let balance = *self.balance - amount;
        self.balance = balance.into();
        if self.balance.is_zero() {
            tracing::debug!(?self, "balance is zero, closing position");
            self.side = PositionSide::None;
        }
        pnl
    }

    #[cfg(not(target_family = "wasm"))]
    pub(crate) fn cross_over(&mut self, price: Decimal, amount: Decimal) -> Result<Decimal> {
        // The pnl is based on the old balance because we're crossing over (closing out that balance)
        let pnl = self.unrealized_pnl(price);
        self.side = match self.side {
            PositionSide::Long => PositionSide::Short,
            PositionSide::Short => PositionSide::Long,
            PositionSide::None => bail!("Cannot cross over empty position"),
        };
        // Subtracting the amount from the balance to close the old position and keep the remaining amount
        let balance = amount - *self.balance;
        self.balance = balance.into();
        // Setting the average entry price because we're opening a new position
        self.avg_entry_price = price.into();
        Ok(pnl)
    }

    /// Calculates the average entry price for this position
    #[cfg(not(target_family = "wasm"))]
    fn calculate_avg_entry_price(&self, price: Decimal, amount: Decimal) -> Decimal {
        let order_price = price;
        let balance = *self.balance;
        let price =
            ((*self.avg_entry_price * balance) + (order_price * amount)) / (balance + amount);
        tracing::trace!(
            "Avg entry px: (({:?} * {:?}) ({:?} + {:?})) = {:?}",
            *self.avg_entry_price,
            balance,
            order_price,
            amount,
            price
        );
        price
    }
}

#[tracing::instrument(level = "debug")]
fn next_price_ema(
    previous_ema: Decimal,
    index_price: Decimal,
    bid: Option<Decimal>,
    ask: Option<Decimal>,
) -> Decimal {
    // If the book is empty, we assume no market so a fair price of zero
    let fair_price = match (bid, ask) {
        (Some(b), Some(a)) => (b + a) / dec!(2),
        (Some(b), None) => b,
        (None, Some(a)) => a,
        (None, None) => index_price,
    };
    let price = index_price;
    let premium = fair_price - price;
    let ema_multiplier = dec!(2) / (*EMA_PERIODS + Decimal::one());
    (premium - previous_ema) * ema_multiplier + previous_ema
}

/// Direction of the price movement compared to the last price update executed.
#[cfg_attr(feature = "python", pyclass(frozen))]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum PriceDirection {
    Up,
    Down,
    Flat, // NOTE 3591: While stale is not wrong, it carries a connotation that the data might be outdated so I renamed it.
    /// Not enough context to determine the direction
    Unknown,
}

impl PriceDirection {
    pub fn from_price_change(price: Decimal, prev: Option<Decimal>) -> Self {
        if let Some(prev) = &prev {
            match price.cmp(prev) {
                core::cmp::Ordering::Less => PriceDirection::Down,
                core::cmp::Ordering::Equal => PriceDirection::Flat,
                core::cmp::Ordering::Greater => PriceDirection::Up,
            }
        } else {
            PriceDirection::Unknown
        }
    }
}

#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[non_exhaustive]
pub enum MarkPriceKind {
    Ema,
    #[cfg(feature = "fixed_expiry_future")]
    Average,
}

/// Metadata for calculating the mark price, along with the current index price
#[derive(Debug, Clone, PartialEq, Deserialize, Serialize, AbiToken, Eq, Copy)]
#[serde(tag = "t", content = "c")]
#[non_exhaustive]
pub enum MarkPriceMetadata {
    /// The mark price is calculated using the ema
    /// The calculated exponential moving address (input to the mark price and verifiable using orderbook snapshot in the aggregate tree)
    Ema(UnscaledI128),
    /// The mark price is calculated as an average using the sum and amount of previous index prices
    /// Mark price = (accum + index_price) / (count + 1)
    #[cfg(feature = "fixed_expiry_future")]
    Average { accum: UnscaledI128, count: u64 },
}

impl Default for MarkPriceMetadata {
    fn default() -> Self {
        MarkPriceMetadata::Ema(UnscaledI128::default())
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for MarkPriceMetadata {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        MarkPriceMetadata::Ema(UnscaledI128::arbitrary(g))
    }
}

#[cfg(feature = "python")]
impl FromPyObject<'_> for MarkPriceMetadata {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        ob.extract::<exported::python::MarkPriceMetadata>()
            .map(Self::from)
    }
}

#[cfg(feature = "python")]
impl IntoPy<PyObject> for MarkPriceMetadata {
    fn into_py(self, py: Python) -> PyObject {
        exported::python::MarkPriceMetadata::from(self).into_py(py)
    }
}

/// A price value (used for funding and liquidations)
#[cfg_attr(feature = "python", pyclass(get_all, set_all))]
#[derive(Debug, Default, Clone, PartialEq, Deserialize, Serialize, AbiToken, Eq, Copy)]
#[serde(rename_all = "camelCase")]
#[repr(C)]
pub struct Price {
    /// The index price number coming from a price feed
    #[serde(with = "as_scaled_fraction")]
    pub index_price: UnscaledI128,
    pub mark_price_metadata: MarkPriceMetadata,
    pub ordinal: u64,
    pub time_value: TimeValue,
}

#[cfg(feature = "python")]
#[pymethods]
impl Price {
    #[new]
    fn new_py(
        index_price: UnscaledI128,
        mark_price_metadata: MarkPriceMetadata,
        ordinal: u64,
        time_value: TimeValue,
    ) -> Self {
        Self {
            index_price,
            mark_price_metadata,
            ordinal,
            time_value,
        }
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for Price {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        Self {
            index_price: UnscaledI128::arbitrary(g),
            mark_price_metadata: Arbitrary::arbitrary(g),
            ordinal: Arbitrary::arbitrary(g),
            time_value: Arbitrary::arbitrary(g),
        }
    }
}

impl VoidableItem for Price {
    fn is_void(&self) -> bool {
        self == &Price::default()
    }
}

impl Price {
    /// Next price with the current value included in the EMA
    pub fn next_ema(
        index_price: Decimal,
        previous_ema: Decimal,
        bid: Option<Decimal>,
        ask: Option<Decimal>,
        ordinal: u64,
        time_value: TimeValue,
    ) -> Self {
        Price {
            index_price: index_price.into(),
            mark_price_metadata: MarkPriceMetadata::Ema(
                next_price_ema(previous_ema, index_price, bid, ask).into(),
            ),
            ordinal,
            time_value,
        }
    }

    /// Next price with new index prices and count
    #[cfg(feature = "fixed_expiry_future")]
    pub fn next_average(
        index_price: Decimal,
        accum: Decimal,
        count: u64,
        ordinal: u64,
        time_value: TimeValue,
    ) -> Self {
        Price {
            index_price: index_price.into(),
            mark_price_metadata: MarkPriceMetadata::Average {
                accum: accum.into(),
                count,
            },
            ordinal,
            time_value,
        }
    }

    #[allow(dead_code)]
    pub(crate) fn from_price_value(
        value: UnscaledI128,
        ordinal: u64,
        time_value: TimeValue,
    ) -> Price {
        Price {
            index_price: value,
            mark_price_metadata: Default::default(),
            ordinal,
            time_value,
        }
    }

    fn index_price(&self) -> UnscaledI128 {
        self.index_price
    }

    pub fn mark_price(&self) -> Decimal {
        let mark_price = match self.mark_price_metadata {
            MarkPriceMetadata::Ema(ema) => {
                let index_price = *self.index_price();
                if ema.is_sign_negative() {
                    let delta = (*ema).max(*FUNDING_LOWER_BOUND * index_price);
                    index_price + delta
                } else {
                    let delta = (*ema).min(*FUNDING_UPPER_BOUND * index_price);
                    index_price + delta
                }
            }
            #[cfg(feature = "fixed_expiry_future")]
            MarkPriceMetadata::Average { accum, count } => {
                (*accum + *self.index_price()) / Decimal::from(count + 1)
            }
        };
        *UnscaledI128::new(mark_price)
    }

    pub fn premium_rate(&self) -> Option<Decimal> {
        match self.mark_price_metadata {
            MarkPriceMetadata::Ema(ema) => Some(*ema / *self.index_price()),
            #[cfg(feature = "fixed_expiry_future")]
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Deserialize, Serialize, AbiToken, Eq)]
#[serde(tag = "t", content = "c")]
#[non_exhaustive]
pub enum PriceMetadata {
    Empty,
    SingleNamePerpetual,
    #[cfg(feature = "index_fund")]
    IndexFundPerpetual(BTreeMap<UnderlyingSymbol, UnscaledI128>),
    #[cfg(feature = "fixed_expiry_future")]
    QuarterlyExpiryFuture,
}

#[cfg(feature = "python")]
impl FromPyObject<'_> for PriceMetadata {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        pythonize::depythonize(ob).map_err(|e| {
            crate::types::state::exported::python::DdxCommonError::new_err(e.to_string())
        })
    }
}

#[cfg(feature = "python")]
impl IntoPy<PyObject> for PriceMetadata {
    fn into_py(self, py: Python) -> PyObject {
        pythonize::pythonize(py, &self).unwrap()
    }
}

#[cfg_attr(feature = "python", pyclass(frozen))]
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum TradeSide {
    Maker,
    Taker,
}

impl TradeSide {
    /// Calculate the trading fee given these trade attributes
    #[tracing::instrument(level = "trace")]
    pub fn trading_fee(&self, amount: Decimal, price: Decimal) -> Decimal {
        let rate = match self {
            TradeSide::Maker => *MAKER_FEE_BPS,
            TradeSide::Taker => *TAKER_FEE_BPS,
        };
        let notional = amount * price;
        let fee = notional * rate;
        tracing::trace!(
            "Calculating {:?} fee - Notional: {:?} * Rate: {:?} = {:?}",
            self,
            notional,
            rate,
            fee
        );
        fee
    }
}

impl fmt::Display for TradeSide {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        // TODO 3503: But why adjusting the case here in the first place?
        match self {
            TradeSide::Maker => write!(f, "maker"),
            TradeSide::Taker => write!(f, "taker"),
        }
    }
}

#[cfg(test)]
pub mod tests {
    use super::*;
    use crate::types::primitives::FixedBytesWrapper;
    #[test]
    fn test_strategy_id_parsing() {
        // Non main strategy
        let non_main_bytes32 = "abcd".parse::<Bytes32>().unwrap();
        let non_main_strat: StrategyId = non_main_bytes32.into();
        assert_eq!(
            non_main_strat,
            StrategyId::from_string("abcd".to_string()).unwrap()
        );

        // invalid utf8 sequence
        let mut invalid_bytes = non_main_bytes32.as_bytes().to_vec();
        invalid_bytes[1] = 255;
        invalid_bytes[2] = 255;
        let invalid_strat: StrategyId = Bytes32::from_slice(invalid_bytes.as_slice()).into();
        assert_eq!(invalid_strat, StrategyId::default());

        //misencoded non main where length byte is missing
        let mut misencoded_bytes_vec = non_main_bytes32.as_bytes().to_vec();
        misencoded_bytes_vec.remove(0);
        misencoded_bytes_vec.resize(32, 0_u8);
        let misencoded_strat: StrategyId =
            Bytes32::from_slice(misencoded_bytes_vec.as_slice()).into();
        assert_eq!(misencoded_strat, StrategyId::default());
    }
}
