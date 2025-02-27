use ddx_common_macros::AbiToken;
#[cfg(feature = "test_harness")]
use ddx_common_macros::unscaled;
#[cfg(feature = "arbitrary")]
use quickcheck::Arbitrary;
use serde::{Deserialize, Serialize};

use crate::{
    Error, Result, error,
    specs::types::SpecsKey,
    types::{
        primitives::{UnderlyingSymbol, UnscaledI128},
        state::{TradableProductKey, TradableProductParameters},
    },
};

use super::eval::{Atom, Expr, StructRepr, eval_from_str};
use chrono::{Duration, prelude::*};

#[cfg(feature = "python")]
use super::extract_field;
#[cfg(feature = "python")]
use pyo3::{prelude::*, types::PyDict};
use std::{fmt, str::FromStr};

#[cfg_attr(feature = "python", pyclass(frozen))]
#[derive(
    Clone,
    Copy,
    Debug,
    PartialEq,
    Eq,
    Deserialize,
    Serialize,
    Default,
    PartialOrd,
    Ord,
    AbiToken,
    std::hash::Hash,
)]
#[repr(u8)]
pub enum Quarter {
    #[default]
    March,
    June,
    September,
    December,
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for Quarter {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        *g.choose(&[
            Quarter::March,
            Quarter::June,
            Quarter::September,
            Quarter::December,
        ])
        .unwrap()
    }
}

impl Quarter {
    pub fn find_quarter(datetime: DateTime<Utc>) -> Self {
        let mut expiry_dates = [
            Quarter::March,
            Quarter::June,
            Quarter::September,
            Quarter::December,
        ]
        .into_iter()
        .map(|quarter| (quarter, quarter.expiry_date(datetime.year())));

        expiry_dates
            .find_map(|(quarter, expiry_date)| {
                if datetime < expiry_date {
                    Some(quarter)
                } else {
                    None
                }
            })
            .unwrap_or(Quarter::March)
    }

    // Finds last Friday of the month and the current year and returns the date at 8:00 am UTC
    fn expiry_date(&self, year: i32) -> DateTime<Utc> {
        let mut date = match self {
            Quarter::March => Utc.with_ymd_and_hms(year, 3, 31, 8, 0, 0),
            Quarter::June => Utc.with_ymd_and_hms(year, 6, 30, 8, 0, 0),
            Quarter::September => Utc.with_ymd_and_hms(year, 9, 30, 8, 0, 0),
            Quarter::December => Utc.with_ymd_and_hms(year, 12, 31, 8, 0, 0),
        }
        .unwrap();
        while date.weekday() != chrono::Weekday::Fri {
            date -= Duration::try_days(1).unwrap();
        }
        date
    }

    // Finds the expiry date of the quarter expiring after the current time on the given quarter month
    pub fn expiry_date_after(&self, current_time: DateTime<Utc>) -> DateTime<Utc> {
        let year = current_time.year();
        let mut date = self.expiry_date(year);
        if current_time > date {
            date = self.expiry_date(year + 1);
        }
        date
    }

    // Finds the upcoming expiry date given the current datetime
    pub fn upcoming_expiry_date(current_time: DateTime<Utc>) -> DateTime<Utc> {
        let mut quarter = Self::find_quarter(current_time);
        let mut year = current_time.year();
        let mut date = quarter.expiry_date(year);
        if current_time > date {
            quarter = quarter.next();
            if quarter == Quarter::March {
                year += 1;
            }
            date = quarter.expiry_date(year);
        }
        date
    }

    pub fn next(&self) -> Quarter {
        match self {
            Quarter::March => Quarter::June,
            Quarter::June => Quarter::September,
            Quarter::September => Quarter::December,
            Quarter::December => Quarter::March,
        }
    }
}

impl fmt::Display for Quarter {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "{}",
            match self {
                Quarter::March => "March",
                Quarter::June => "June",
                Quarter::September => "September",
                Quarter::December => "December",
            }
        )
    }
}

impl From<&str> for Quarter {
    fn from(value: &str) -> Self {
        value.parse().unwrap()
    }
}

impl FromStr for Quarter {
    type Err = Error;
    fn from_str(value: &str) -> Result<Self, Self::Err> {
        Ok(match value {
            "March" => Quarter::March,
            "June" => Quarter::June,
            "September" => Quarter::September,
            "December" => Quarter::December,
            _ => return Err(Error::Parse("Invalid quarter".to_string())),
        })
    }
}

impl From<char> for Quarter {
    fn from(value: char) -> Self {
        match value {
            'H' => Quarter::March,
            'M' => Quarter::June,
            'U' => Quarter::September,
            'Z' => Quarter::December,
            _ => panic!("Invalid quarter"),
        }
    }
}

impl From<Quarter> for char {
    fn from(value: Quarter) -> Self {
        match value {
            Quarter::March => 'H',
            Quarter::June => 'M',
            Quarter::September => 'U',
            Quarter::December => 'Z',
        }
    }
}

impl TryFrom<Atom> for Quarter {
    type Error = Error;

    fn try_from(value: Atom) -> Result<Self, Self::Error> {
        if let Atom::Str(v) = value {
            Ok(v.as_str().into())
        } else {
            Err(error!("Wrong type {:?}", value))
        }
    }
}

/// Quarterly expiry futures are contracts that expire at a month 28-day basis.
///
/// This only include attributes common to all quarterly expiry futures.
#[cfg_attr(feature = "python", pyclass(frozen, get_all))]
#[derive(Clone, Debug, PartialEq, Deserialize, Serialize, Eq)]
#[serde(rename_all = "camelCase")]
pub struct QuarterlyExpiryFuture {
    pub underlying: UnderlyingSymbol,
    pub tick_size: UnscaledI128,
    pub max_order_notional: UnscaledI128,
    pub max_taker_price_deviation: UnscaledI128,
    pub min_order_size: UnscaledI128,
}

#[cfg(feature = "python")]
#[pymethods]
impl QuarterlyExpiryFuture {
    #[new]
    #[pyo3(signature = (**kwds))]
    pub(crate) fn new_py(kwds: Option<&PyDict>) -> PyResult<Self> {
        let kwds = kwds.ok_or_else(|| {
            crate::types::state::exported::python::DdxCommonError::new_err(
                "Expected keyword dictionary containing specs".to_string(),
            )
        })?;
        Ok(Self {
            underlying: extract_field(kwds, "underlying")?,
            tick_size: extract_field(kwds, "tick_size")?,
            max_order_notional: extract_field(kwds, "max_order_notional")?,
            max_taker_price_deviation: extract_field(kwds, "max_taker_price_deviation")?,
            min_order_size: extract_field(kwds, "min_order_size")?,
        })
    }
}

#[cfg(feature = "test_harness")]
impl Default for QuarterlyExpiryFuture {
    fn default() -> Self {
        QuarterlyExpiryFuture {
            underlying: "ETH".into(),
            tick_size: unscaled!(0.1),
            max_order_notional: unscaled!(1_000_000),
            max_taker_price_deviation: unscaled!(0.02),
            min_order_size: unscaled!(0.000_1),
        }
    }
}

impl QuarterlyExpiryFuture {
    pub(crate) fn current_tradable_products(
        specs: SpecsKey,
        current_time: DateTime<Utc>,
    ) -> Vec<TradableProductKey> {
        // There will always be at least two tradable quarterly futures at any time: the current and
        // next quarters.
        // There will be exactly three exactly one week before expiry of any future. The extra
        // future is two quarters ahead.
        // The expiry date of any quarter is always the last Friday of the month at 8:00 am UTC.
        let mut tradable_products = Vec::with_capacity(3);
        let current_quarter = Quarter::find_quarter(current_time);
        tradable_products.push(TradableProductKey {
            specs: specs.clone(),
            parameters: Some(TradableProductParameters::QuarterlyExpiryFuture(
                current_quarter,
            )),
        });
        tradable_products.push(TradableProductKey {
            specs: specs.clone(),
            parameters: Some(TradableProductParameters::QuarterlyExpiryFuture(
                current_quarter.next(),
            )),
        });

        let upcoming_expiry_date = current_quarter.expiry_date_after(current_time);
        if upcoming_expiry_date - current_time <= Duration::try_weeks(1).unwrap() {
            tradable_products.push(TradableProductKey {
                specs: specs.clone(),
                parameters: Some(TradableProductParameters::QuarterlyExpiryFuture(
                    current_quarter.next().next(),
                )),
            });
        }

        tradable_products
    }
}

/// Shorthand parser that panics on error.
impl<T: AsRef<str>> From<T> for QuarterlyExpiryFuture {
    fn from(expr: T) -> Self {
        let expr = expr.as_ref();
        expr.parse().expect("Invalid market specs")
    }
}

impl FromStr for QuarterlyExpiryFuture {
    type Err = Error;

    fn from_str(expr: &str) -> Result<Self, Self::Err> {
        if let Expr::Constant(Atom::Struct(repr)) = eval_from_str(expr)? {
            repr.try_into()
        } else {
            Err(Error::Parse(expr.to_string()))
        }
    }
}

impl TryFrom<StructRepr> for QuarterlyExpiryFuture {
    type Error = Error;

    fn try_from(mut repr: StructRepr) -> Result<Self, Self::Error> {
        repr.ensure_match("QuarterlyExpiryFuture", 6)?;
        Ok(QuarterlyExpiryFuture {
            underlying: repr.try_take("underlying")?.try_into()?,
            tick_size: repr.try_take("tick-size")?.try_into()?,
            max_order_notional: repr.try_take("max-order-notional")?.try_into()?,
            max_taker_price_deviation: repr.try_take("max-taker-price-deviation")?.try_into()?,
            min_order_size: repr.try_take("min-order-size")?.try_into()?,
        })
    }
}
