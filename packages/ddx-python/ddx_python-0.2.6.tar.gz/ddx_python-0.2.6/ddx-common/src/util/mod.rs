use crate::Result;
use chrono::{DateTime, Utc};
use rust_decimal::{
    Decimal,
    prelude::{FromPrimitive, One},
};
use std::{
    convert::TryInto,
    time::{Duration, UNIX_EPOCH},
};

#[cfg(all(not(target_vendor = "teaclave"), not(target_family = "wasm")))]
pub mod backoff;
#[cfg(not(target_family = "wasm"))]
pub(crate) mod convert;
#[cfg(not(target_family = "wasm"))]
pub mod eip712;
#[cfg(not(target_family = "wasm"))]
pub mod enclave;
#[cfg(not(target_family = "wasm"))]
pub mod env;
#[cfg(not(target_family = "wasm"))]
pub mod mem;
#[cfg(all(not(target_vendor = "teaclave"), not(target_family = "wasm")))]
pub mod node;
pub mod serde;
pub mod tokenize;
pub mod tracing;

/// The default trade mining reward per epoch. This is the amount that will be
/// used in production, and will be used throughout our tests.
///
/// This is calculated as 35,000,000 / (3 * 10 * 365). This is 35 million
/// divided by the number of epochs of trade mining that will occur (3 per
/// day 365 days a year for 10 years).
pub fn default_trade_mining_reward_per_epoch() -> Decimal {
    Decimal::from(35000000) / (Decimal::from(3) * Decimal::from(10) * Decimal::from(365))
}

pub fn default_trade_mining_maker_reward_percentage() -> Decimal {
    Decimal::from_f32(0.2).unwrap()
}

pub fn default_trade_mining_taker_reward_percentage() -> Decimal {
    Decimal::one() - default_trade_mining_maker_reward_percentage()
}

pub fn unix_timestamp_to_datetime(unix_timestamp: i64) -> Result<DateTime<Utc>> {
    Ok(DateTime::<Utc>::from(
        UNIX_EPOCH + Duration::from_secs(unix_timestamp.try_into()?),
    ))
}
