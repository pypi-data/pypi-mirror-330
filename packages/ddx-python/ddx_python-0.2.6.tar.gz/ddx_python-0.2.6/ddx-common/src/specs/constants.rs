use ddx_common_macros::dec;
use lazy_static::lazy_static;
use rust_decimal::Decimal;

// TODO: Some of the values in this file should ultimately be moved into
// contract specs.

lazy_static! {
    pub static ref FUNDING_ZERO_UPPER_BOUND: Decimal = dec!(0.0005);
    pub static ref FUNDING_ZERO_LOWER_BOUND: Decimal = dec!(-0.0005);
    pub static ref FUNDING_UPPER_BOUND: Decimal = dec!(0.005);
    pub static ref FUNDING_LOWER_BOUND: Decimal = dec!(-0.005);
}
