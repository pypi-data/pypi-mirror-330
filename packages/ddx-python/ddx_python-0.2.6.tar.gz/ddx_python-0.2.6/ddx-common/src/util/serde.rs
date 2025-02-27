use serde::{
    de::{Deserialize, Deserializer, Error as DeError, Visitor},
    ser::{Error, Serialize, Serializer},
};
use std::{collections::HashMap, fmt};

pub mod as_scaled_fraction {
    use super::*;
    use crate::types::primitives::UnscaledI128;
    use std::convert::TryFrom;

    // Serialize scaled fraction to an unscaled float.
    pub fn serialize<T, S>(value: &T, serializer: S) -> Result<S::Ok, S::Error>
    where
        // All number kinds implement copy
        T: Into<UnscaledI128> + Copy,
        S: Serializer,
    {
        // Normalizing the decimal when serializing numbers into string to use the simplest
        // representation instead a zero padded scheme
        let d = UnscaledI128::from(value);
        let v = serde_json::to_value(d).map_err(S::Error::custom)?;
        v.serialize(serializer)
    }

    // Deserialize float into scaled integer.
    pub fn deserialize<'de, T, D>(deserializer: D) -> Result<T, D::Error>
    where
        T: From<UnscaledI128>,
        D: Deserializer<'de>,
    {
        // Try to deserialize any string (by trying to parse it) or number types.
        let v = serde_json::Value::deserialize(deserializer)?;
        // TODO 1208: Is this enough to prevent all numeric overflows with external inputs
        let d = UnscaledI128::try_from(v).map_err(D::Error::custom)?;
        Ok(d.into())
    }
}

pub mod as_u64 {
    use super::*;
    use crate::ethereum_types::U64;

    // Unwrap `U64` and serialize
    pub fn serialize<S>(value: &U64, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let num = value.low_u64();
        let ser = serde_json::to_value(num).map_err(S::Error::custom)?;
        ser.serialize(serializer)
    }

    // Deserialize and wrap `U64`
    pub fn deserialize<'de, D>(deserializer: D) -> Result<U64, D::Error>
    where
        D: Deserializer<'de>,
    {
        let num: u64 = Deserialize::deserialize(deserializer)?;
        Ok(U64::from(num))
    }
}

pub mod as_bytes4_hex {
    use super::*;
    use crate::types::{identifiers::StrategyIdHash, primitives::FixedBytesWrapper};
    use rustc_hex::{FromHex, ToHex};

    pub fn serialize<S>(value: &[u8; 4], serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let hex = format!("0x{}", value.as_slice().to_hex::<String>());
        hex.serialize(serializer)
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<[u8; 4], D::Error>
    where
        D: Deserializer<'de>,
    {
        let hex: String = Deserialize::deserialize(deserializer)?;
        let bytes: Vec<u8> = hex.replace("0x", "").from_hex().map_err(D::Error::custom)?;
        StrategyIdHash::copy_fixed_bytes(&bytes).map_err(D::Error::custom)
    }
}

pub mod as_bytes25_hex {
    use super::*;
    use crate::types::primitives::{Bytes25, FixedBytesWrapper};
    use rustc_hex::{FromHex, ToHex};

    pub fn serialize<S>(value: &[u8; 25], serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let hex = format!("0x{}", value.as_slice().to_hex::<String>());
        hex.serialize(serializer)
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<[u8; 25], D::Error>
    where
        D: Deserializer<'de>,
    {
        let hex: String = Deserialize::deserialize(deserializer)?;
        let mut bytes: Vec<u8> = hex.replace("0x", "").from_hex().map_err(D::Error::custom)?;
        if bytes.len() < 25 {
            bytes.resize(25, 0_u8);
        }
        Bytes25::copy_fixed_bytes(&bytes).map_err(D::Error::custom)
    }
}

pub mod as_bytes65_hex {
    use super::*;
    use crate::types::primitives::{FixedBytesWrapper, Signature};
    use rustc_hex::{FromHex, ToHex};

    pub fn serialize<S>(value: &[u8; 65], serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let hex = format!("0x{}", value.as_slice().to_hex::<String>());
        hex.serialize(serializer)
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<[u8; 65], D::Error>
    where
        D: Deserializer<'de>,
    {
        let hex: String = Deserialize::deserialize(deserializer)?;
        let mut bytes: Vec<u8> = hex.replace("0x", "").from_hex().map_err(D::Error::custom)?;
        if bytes.len() < 65 {
            bytes.resize(65, 0_u8);
        }
        Signature::copy_fixed_bytes(&bytes).map_err(D::Error::custom)
    }
}

pub mod as_underlying_symbol {
    use super::*;
    use crate::types::primitives::UnderlyingSymbol;

    pub fn serialize<S>(value: &[u8; 4], serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let text = std::str::from_utf8(value.trim_ascii_end()).map_err(S::Error::custom)?;
        text.serialize(serializer)
    }

    struct AsciiBytesVisitor;

    impl Visitor<'_> for AsciiBytesVisitor {
        type Value = [u8; 4];

        fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
            formatter.write_str("A fixed length 4-byte array of ASCII characters")
        }

        fn visit_str<E: serde::de::Error>(self, text: &str) -> Result<Self::Value, E> {
            UnderlyingSymbol::from_ascii_bytes(text.as_bytes())
                .map(|symbol| symbol.0)
                .map_err(serde::de::Error::custom)
        }
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<[u8; 4], D::Error>
    where
        D: Deserializer<'de>,
    {
        deserializer.deserialize_str(AsciiBytesVisitor)
    }
}

pub mod as_product_symbol {
    use super::*;
    use crate::types::primitives::ProductSymbol;

    pub fn serialize<S>(value: &[u8; 6], serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        // Serializing as string by unpacking using our custom scheme
        let text = ProductSymbol::unpack_bytes(value).map_err(S::Error::custom)?;
        text.serialize(serializer)
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<[u8; 6], D::Error>
    where
        D: Deserializer<'de>,
    {
        // Deserialize into string then storing using our custom bit packing scheme
        let text: String = Deserialize::deserialize(deserializer)?;
        ProductSymbol::parse_parts(&text)
            .map(|(s, p)| ProductSymbol::pack_bytes(s, p))
            .map_err(D::Error::custom)
    }
}

pub mod as_specs {

    use super::*;
    use crate::specs::types::{Specs, SpecsExpr};

    pub fn serialize<S>(value: &Specs, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let labeled = value
            .iter()
            .map(|(k, v)| (k.to_string(), v))
            .collect::<HashMap<_, _>>();
        labeled.serialize(serializer)
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<Specs, D::Error>
    where
        D: Deserializer<'de>,
    {
        let labeled: HashMap<String, SpecsExpr> = Deserialize::deserialize(deserializer)?;
        let mut specs = HashMap::default();
        for (l, v) in labeled {
            match l.parse() {
                Ok(k) => {
                    specs.insert(k, v);
                }
                Err(e) => {
                    tracing::error!(?e, "Invalid specs expression");
                }
            }
        }
        Ok(specs)
    }
}

pub mod as_bytes33_hex {
    use super::*;
    use crate::types::primitives::{Bytes33, FixedBytesWrapper};
    use rustc_hex::{FromHex, ToHex};

    pub fn serialize<S>(value: &[u8; 33], serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let hex = format!("0x{}", value.as_slice().to_hex::<String>());
        hex.serialize(serializer)
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<[u8; 33], D::Error>
    where
        D: Deserializer<'de>,
    {
        let hex: String = Deserialize::deserialize(deserializer)?;
        let mut bytes: Vec<u8> = hex.replace("0x", "").from_hex().map_err(D::Error::custom)?;
        if bytes.len() < 33 {
            bytes.resize(33, 0_u8);
        }
        Bytes33::copy_fixed_bytes(&bytes).map_err(D::Error::custom)
    }
}

pub mod as_address_hex {
    use super::*;
    use crate::{
        constants::CHAIN_ETHEREUM,
        types::primitives::{Bytes21, FixedBytesWrapper},
    };
    use rustc_hex::{FromHex, ToHex};

    pub fn serialize<S>(value: &[u8; 21], serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        if value.len() != 21 {
            return Err(anyhow::anyhow!(
                "Expected a 21 bytes 0x prefixed hex string - Got {} bytes",
                value.len()
            ))
            .map_err(S::Error::custom);
        }
        let hex = format!("0x{}", value.as_slice().to_hex::<String>());
        hex.serialize(serializer)
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<[u8; 21], D::Error>
    where
        D: Deserializer<'de>,
    {
        let hex: String = Deserialize::deserialize(deserializer)?;
        let mut bytes: Vec<u8> = hex.replace("0x", "").from_hex().map_err(D::Error::custom)?;
        // As a convenience, we assume that 20 bytes addresses are Ethereum accounts.
        // This may be deprecated at any time when adding other chains so always ask clients
        // to explicitly include the chain discriminant.
        if bytes.len() == 20 {
            bytes.insert(0, CHAIN_ETHEREUM);
        }
        if bytes.len() != 21 {
            return Err(anyhow::anyhow!(
                "Expected a 21 bytes 0x prefixed hex string - Got {} bytes",
                bytes.len()
            ))
            .map_err(D::Error::custom);
        }
        Bytes21::copy_fixed_bytes(&bytes).map_err(D::Error::custom)
    }
}

/// This module is for serialization of strategy id stored as bytes32.
pub mod as_bytes32_text {
    use super::*;
    use crate::types::primitives::Bytes32;
    use core::{fmt, str::FromStr};
    use serde::de::Visitor;
    struct StrategyIdVisitor;

    impl Visitor<'_> for StrategyIdVisitor {
        type Value = Bytes32;
        fn visit_str<E>(self, v: &str) -> core::result::Result<Self::Value, E>
        where
            E: DeError,
        {
            Bytes32::from_str(v).map_err(|_e| DeError::invalid_length(v.len(), &self))
        }

        fn visit_string<E>(self, v: String) -> Result<Self::Value, E>
        where
            E: DeError,
        {
            self.visit_str(&v)
        }

        fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
            formatter.write_str("An string take less than 32 bytes")
        }
    }

    pub fn serialize<S>(value: &Bytes32, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        serializer.serialize_str(&value.to_string())
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<Bytes32, D::Error>
    where
        D: Deserializer<'de>,
    {
        deserializer.deserialize_string(StrategyIdVisitor)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::ethereum_types::U128;
    use rust_decimal::Decimal;
    use serde::{Deserialize, Serialize};
    use serde_json::json;

    #[derive(Serialize, Deserialize)]
    struct ScaledFraction {
        /// Deserializes a decimal value into integer by scaling it up: I=D**18
        #[serde(with = "as_scaled_fraction")]
        pub value: U128,
    }

    #[test]
    fn test_scaled_fractions() {
        let message = json!({ "value": "1234.4444" });
        let _res: ScaledFraction = serde_json::from_value(message).unwrap();
        let message = json!({ "value": "1234" });
        let _res: ScaledFraction = serde_json::from_value(message).unwrap();
        let message = json!({ "value": ".4444" });
        let _res: ScaledFraction = serde_json::from_value(message).unwrap();
    }

    #[test]
    fn test_bad_scaled_fractions() {
        let max_dec = format!("{}", Decimal::MAX.floor());
        let message = json!({ "value": max_dec });
        let maybe_s: Result<ScaledFraction, _> = serde_json::from_value(message);
        if maybe_s.is_ok() {
            panic!(
                "Expected number greater than MAX_UNSCALED_DECIMAL to be caught by our deserializer max_dec={}",
                max_dec
            )
        }
        let fract = "79228162514264337593543950335.994276";
        let message = json!({ "value": fract });
        let maybe_s: Result<ScaledFraction, _> = serde_json::from_value(message);
        if maybe_s.is_ok() {
            panic!("Expected failure");
        }
        // Being left-aligned, the number is either truncated or filled with zeroes.
        let over_dec = format!(
            "{:0<width$}",
            max_dec,
            // Append zeroes to cause overflow
            width = max_dec.len() + 1
        );
        let message = json!({ "value": over_dec });
        let maybe_s: Result<ScaledFraction, _> = serde_json::from_value(message);
        if maybe_s.is_ok() {
            panic!(
                "Expected number greater than Decimal::MAX to be caught by Decimal's deserializer over_dec={}",
                over_dec
            )
        }
    }

    #[test]
    fn test_bad_decimal() {
        let fract = "79228162514264337593543950335.994276";
        let res: Result<Decimal, _> = serde_json::from_str(fract);
        if let Err(err) = res {
            println!("Handled deserialization error {}", err);
        }
    }
}
