#[cfg(feature = "arbitrary")]
use crate::types::identifiers::arbitrary_h160;
use crate::{
    Error, Result, bail,
    constants::{CHAIN_ETHEREUM, KECCAK256_DIGEST_SIZE},
    crypto::{Keccak256, from_hex},
    ensure, error,
    ethabi::Token,
    ethereum_types::{Address, H256 as EthH256, H520, U128, U256},
    util::{
        serde::{
            as_address_hex, as_bytes25_hex, as_bytes33_hex, as_bytes65_hex, as_product_symbol,
            as_scaled_fraction, as_underlying_symbol,
        },
        tokenize::Tokenizable,
    },
};
use bitvec::{
    prelude::{BitSlice, Lsb0},
    vec::BitVec,
};
use chrono::{DateTime, Utc};
use ddx_common_macros::{AbiToken, AsKeccak256};
use lazy_static::lazy_static;
#[cfg(feature = "database")]
use postgres_types::{FromSql, IsNull, ToSql, Type, to_sql_checked};
#[cfg(feature = "python")]
use pyo3::prelude::*;
#[cfg(feature = "arbitrary")]
use quickcheck::Arbitrary;
use regex::Regex;
use rustc_hex::ToHex;
use serde::{Deserialize, Serialize};
use sparse_merkle_tree::h256::H256;
use std::{
    fmt::{self, Formatter},
    mem::size_of,
    str::{FromStr, from_utf8},
    time::SystemTime,
};

pub mod numbers;
pub use numbers::*;

const SYMBOL_CHARSET: &str = "0ABCDEFGHIJKLMNOPQRSTUVWXYZ";

lazy_static! {
    /// Regex for HTTP URLs (not IPv6 compatible) with optional port and path
    static ref URL_RE: Regex =
        Regex::new(r"^http(?P<s>s)?://(?P<h>[a-z0-9\.\-]+)(?P<p>:\d+)?(/[a-z0-9\.\-]*)*$")
            .expect("Invalid URL regex");
}

// Aliasing commonly used primitives for business context.
pub type TraderAddress = Bytes21;
pub type EpochId = u64;
pub type CustodianAddress = Bytes21;
pub type OrderHash = Bytes25;
pub type IndexPriceHash = Bytes25;
pub type TimeValue = u64;

// TODO 3768: This fundamentally depends on app_context so isn't a primitive. Move with related types.
#[derive(
    Clone, PartialOrd, Ord, Debug, PartialEq, Hash, Eq, Deserialize, Serialize, AbiToken, Copy,
)]
pub struct TokenAddress(Address);

#[cfg(feature = "python")]
impl FromPyObject<'_> for TokenAddress {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let hex = ob.extract::<String>()?;
        Ok(Self(Address::from_str(&hex).map_err(|e| {
            crate::types::state::exported::python::DdxCommonError::new_err(e.to_string())
        })?))
    }
}

#[cfg(feature = "python")]
impl IntoPy<PyObject> for TokenAddress {
    fn into_py(self, py: Python) -> PyObject {
        self.to_string().into_py(py)
    }
}

impl FromStr for TokenAddress {
    type Err = <Address as FromStr>::Err;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let hash = Address::from_str(s)?;
        Ok(Self(hash))
    }
}

impl fmt::Display for TokenAddress {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "0x{}", self.0.as_bytes().to_hex::<String>())
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for TokenAddress {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        TokenAddress(arbitrary_h160(g))
    }
}

impl TokenAddress {
    pub fn collateral(address: Address) -> Self {
        crate::global::app_context()
            .collateral_addresses
            .iter()
            .find_map(|(_, collateral_addr)| {
                if collateral_addr == &address {
                    Some(TokenAddress(address))
                } else {
                    None
                }
            })
            .unwrap()
    }

    pub fn ddx() -> Self {
        TokenAddress(crate::global::app_context().ddx_token_address)
    }

    fn new(address: Address) -> Self {
        TokenAddress(address)
    }
}

impl From<TokenAddress> for Address {
    fn from(value: TokenAddress) -> Self {
        value.0
    }
}

impl From<TokenSymbol> for TokenAddress {
    fn from(symbol: TokenSymbol) -> Self {
        if symbol == TokenSymbol::DDX {
            return TokenAddress::new(crate::global::app_context().ddx_token_address);
        }
        TokenAddress::new(crate::global::app_context().collateral_addresses[&symbol])
    }
}

impl From<TokenAddress> for Bytes32 {
    fn from(value: TokenAddress) -> Self {
        const PAD_LEN: usize = Bytes32::BYTE_LEN - size_of::<TokenAddress>();
        let mut padded = vec![0_u8; PAD_LEN];
        padded.extend_from_slice(&(value.0).0);
        let mut slice = [0_u8; Bytes32::BYTE_LEN];
        slice.copy_from_slice(&padded);
        Bytes32::from(slice)
    }
}

#[cfg(feature = "database")]
impl ToSql for TokenAddress {
    fn to_sql(
        &self,
        ty: &Type,
        out: &mut bytes::BytesMut,
    ) -> Result<IsNull, Box<dyn std::error::Error + 'static + Sync + Send>> {
        self.0.as_bytes().to_sql(ty, out)
    }

    fn accepts(ty: &Type) -> bool {
        <&[u8] as ToSql>::accepts(ty)
    }

    to_sql_checked!();
}

/// Well-known ERC20 tokens used in the underpinning of the protocol
#[cfg_attr(feature = "python", pyclass(frozen))]
#[derive(Debug, Clone, Copy, Hash, PartialEq, Serialize, Deserialize, Eq)]
pub enum TokenSymbol {
    USDC,
    DDX,
}

impl fmt::Display for TokenSymbol {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:?}", self)
    }
}

impl From<TokenAddress> for TokenSymbol {
    fn from(value: TokenAddress) -> Self {
        let address = value.0;
        crate::global::app_context()
            .collateral_addresses
            .iter()
            .find_map(|(symbol, collateral_addr)| {
                if collateral_addr == &address {
                    Some(*symbol)
                } else {
                    None
                }
            })
            .unwrap()
    }
}

/// Symbol of the underlying asset, usually a spot market symbol
///
/// This holds 4 bytes representing ASCII characters. If the symbol is shorter than 4 bytes, it is
/// is suffix padded with zeros.
///
/// There's no imperative to pack the underlying symbol bytes like with the product symbol, so we don't.
#[derive(
    Clone, Copy, Default, PartialEq, Eq, std::hash::Hash, PartialOrd, Ord, Deserialize, Serialize,
)]
pub struct UnderlyingSymbol(#[serde(with = "as_underlying_symbol")] pub(crate) [u8; 4]);

#[cfg(feature = "python")]
impl FromPyObject<'_> for UnderlyingSymbol {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let string: String = ob.extract()?;
        Ok(string.parse()?)
    }
}

#[cfg(feature = "python")]
impl IntoPy<PyObject> for UnderlyingSymbol {
    fn into_py(self, py: Python) -> PyObject {
        self.to_string().into_py(py)
    }
}

impl FromStr for UnderlyingSymbol {
    type Err = Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        UnderlyingSymbol::from_ascii_bytes(s.as_bytes())
    }
}

impl From<&str> for UnderlyingSymbol {
    fn from(value: &str) -> Self {
        value.parse().unwrap()
    }
}

impl fmt::Display for UnderlyingSymbol {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "{}", from_utf8(self.trim()).unwrap())
    }
}

impl fmt::Debug for UnderlyingSymbol {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_tuple("UnderlyingSymbol")
            .field(&self.to_string())
            .finish()
    }
}

impl Tokenizable for UnderlyingSymbol {
    fn from_token(token: Token) -> Result<Self>
    where
        Self: Sized,
    {
        let text = Bytes32::from_token(token)?.to_string();
        text.parse()
    }

    fn into_token(self) -> Token {
        let bytes = Bytes32::from(self);
        bytes.into_token()
    }
}

impl From<UnderlyingSymbol> for Bytes32 {
    fn from(value: UnderlyingSymbol) -> Self {
        // Delegate the conversion to the string type
        // Can't fail because we know that the length fits in 32 bytes
        value.to_string().parse().unwrap()
    }
}

impl UnderlyingSymbol {
    pub const BYTE_LEN: usize = size_of::<Self>();

    /// Return a ASCII bytes slice excluding whitespace
    pub(super) fn trim(&self) -> &[u8] {
        self.0.trim_ascii_end()
    }

    /// Tries to encode the given ASCII bytes into the 4 byte symbol convention
    ///
    /// This means ending with whitespace if needed and validating against the character subset.
    #[tracing::instrument(level = "trace", fields(text=?from_utf8(ascii_bytes)))]
    pub(crate) fn from_ascii_bytes(ascii_bytes: &[u8]) -> Result<Self> {
        if ascii_bytes.len() > Self::BYTE_LEN {
            return Err(Error::Parse(format!(
                "Expected up to {} ASCII characters for underlying symbol; got {:?}",
                Self::BYTE_LEN,
                from_utf8(ascii_bytes)
            )));
        }
        let mut bytes = [0_u8; Self::BYTE_LEN];
        for i in 0..bytes.len() {
            if i < ascii_bytes.trim_ascii_end().len() {
                // Allows the type system to guarantee that this is usable as the root of `ProductSymbol`.
                if !SYMBOL_CHARSET.contains(ascii_bytes[i] as char) {
                    return Err(Error::Conversion(format!(
                        "Illegal character in {} charset={}",
                        ascii_bytes[i], SYMBOL_CHARSET
                    )));
                }
                bytes[i] = ascii_bytes[i];
            } else {
                bytes[i] = 32;
            }
        }
        Ok(UnderlyingSymbol(bytes))
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for UnderlyingSymbol {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        let sizes = (2..4).collect::<Vec<i32>>();
        let size = *g.choose(&sizes).unwrap();
        let symbol: String = (0..size)
            .map(|_| {
                // FIXME: Revisit the inclusion of '0' in the charset
                let charset = SYMBOL_CHARSET
                    .chars()
                    .filter(|c| c != &'0')
                    .collect::<Vec<char>>();
                g.choose(&charset).cloned().unwrap()
            })
            .collect();
        symbol.parse().unwrap()
    }
}

/// The kinds of derivative products that can be traded on the exchange
#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize, Serialize)]
#[non_exhaustive]
pub enum Product {
    Perpetual,
    #[cfg(feature = "fixed_expiry_future")]
    QuarterlyExpiryFuture {
        month_code: char,
    },
}

impl fmt::Display for Product {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{}",
            match self {
                Product::Perpetual => "P".to_string(),
                #[cfg(feature = "fixed_expiry_future")]
                Product::QuarterlyExpiryFuture { month_code } => format!("F{}", month_code),
            }
        )
    }
}

impl Product {
    pub const BYTE_LEN: usize = 3;

    fn split(&self) -> (char, Option<char>) {
        match self {
            Product::Perpetual => ('P', None),
            #[cfg(feature = "fixed_expiry_future")]
            Product::QuarterlyExpiryFuture { month_code } => ('F', Some(*month_code)),
        }
    }

    #[tracing::instrument(level = "debug", fields(?bytes))]
    fn from_fixed_bytes(bytes: [u8; Self::BYTE_LEN]) -> Result<Product> {
        let kind = bytes[0];
        match kind {
            b'P' => Ok(Product::Perpetual),
            #[cfg(feature = "fixed_expiry_future")]
            b'F' => {
                let month_code = bytes[1] as char;
                Ok(Product::QuarterlyExpiryFuture { month_code })
            }
            _ => Err(Error::Parse(format!("Unknown product kind {}", kind))),
        }
    }

    /// Tries to construct a Product from the given ASCII bytes
    #[tracing::instrument(level = "debug", fields(text=?from_utf8(ascii_bytes)))]
    fn from_ascii_bytes(ascii_bytes: &[u8]) -> Result<Self> {
        let kind = ascii_bytes.first().ok_or_else(|| {
            Error::Parse(format!(
                "Expected at least 1 ASCII character for underlying symbol; got {:?}",
                from_utf8(ascii_bytes)
            ))
        })?;
        match kind {
            b'P' => Ok(Product::Perpetual),
            #[cfg(feature = "fixed_expiry_future")]
            b'F' => {
                let month_code = ascii_bytes
                    .get(1)
                    .ok_or_else(|| {
                        Error::Parse(format!(
                            "Expected more characters to represent days until expiry, got {:?}",
                            from_utf8(ascii_bytes)
                        ))
                    })
                    .and_then(|&params| {
                        from_utf8(&[params])
                            .map_err(|_| Error::Parse("Expected a utf8 string".to_string()))
                            .map(|params| params.chars().next().unwrap())
                    })?;
                Ok(Product::QuarterlyExpiryFuture { month_code })
            }
            _ => Err(Error::Parse(format!("Unknown product kind {}", kind))),
        }
    }
}

/// Symbol of a product (derivative contract) traded on the exchange
///
/// This symbol is packed into 6 bytes using a custom "5-bit scheme" to adhere to space limitation.
///
/// When unpacked into regular ASCII, the first 3-4 bytes are the root (underlying symbol) followed by one character for the product kind.
/// For example, the symbol for a perpetual contract on BTC would be `BTCP`.
///
/// Some products, like options, may additional digits to reference externally defined attributes like strike price and date.
#[derive(Clone, Copy, PartialEq, Eq, std::hash::Hash, PartialOrd, Ord, Deserialize, Serialize)]
pub struct ProductSymbol(#[serde(with = "as_product_symbol")] pub [u8; 6]);

// TODO: this should be feature gated behind development
impl Default for ProductSymbol {
    fn default() -> Self {
        "ETHP".into()
    }
}

#[cfg(feature = "python")]
impl FromPyObject<'_> for ProductSymbol {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let str_repr = if let Ok(symbol) =
            ob.extract::<crate::types::state::exported::python::ProductSymbol>()
        {
            symbol.to_string()
        } else {
            ob.extract::<String>()?
        };
        Ok(Self::from_str(&str_repr)?)
    }
}

#[cfg(feature = "python")]
impl IntoPy<PyObject> for ProductSymbol {
    fn into_py(self, py: Python) -> PyObject {
        crate::types::state::exported::python::ProductSymbol::from(self).into_py(py)
    }
}

impl ProductSymbol {
    pub const BYTE_LEN: usize = size_of::<Self>();
    // Collect ASCII bytes from the parts; currently limited to 5 bytes but this will change we define more products.
    const ASCII_LEN: usize = 5;

    #[cfg(feature = "arbitrary")]
    pub(super) fn new(underlying: UnderlyingSymbol, product: Product) -> Self {
        ProductSymbol(ProductSymbol::pack_bytes(underlying, product))
    }

    pub fn product(&self) -> Product {
        self.split().1
    }

    /// Parse the parts (underlying symbol and product) from the given ASCII string
    ///
    /// This avoids unnecessarily encoding and decoding an intermediary product symbol.
    #[tracing::instrument(level = "trace")]
    pub(crate) fn parse_parts(text: &str) -> Result<(UnderlyingSymbol, Product)> {
        if text.len() < 2 {
            return Err(Error::Parse(
                "Expected at least 2 characters for product symbol".to_string(),
            ));
        }

        // Find either "P" or "F" from the back
        let product_start_index = text.len()
            - (text
                .chars()
                .rev()
                .position(|c| c == 'P' || c == 'F')
                .ok_or_else(|| {
                    Error::Parse("Expected a character representing the product type".to_string())
                })?
                + 1);

        let bytes = text.as_bytes();
        let u_bytes = &bytes[..product_start_index];
        let p_bytes = &bytes[product_start_index..];
        Ok((
            UnderlyingSymbol::from_ascii_bytes(u_bytes)?,
            Product::from_ascii_bytes(p_bytes)?,
        ))
    }

    /// Convert to ASCII bytes then extract the underlying symbol and product
    pub(crate) fn split(&self) -> (UnderlyingSymbol, Product) {
        // TODO: Split this fn to return a slice of ascii bytes instead of a String
        ProductSymbol::unpack_bytes(&self.0)
            .and_then(|t| ProductSymbol::parse_parts(&t))
            .expect("Unpacking bytes from a ProductSymbol should never fail")
    }

    /// Try to create from a bytes slice packed with the 5-bit scheme
    pub(super) fn from_slice(bytes: &[u8]) -> Result<Self> {
        debug_assert_eq!(
            bytes.len(),
            Self::BYTE_LEN,
            "Expected symbol size to be 6 bytes"
        );
        let mut fixed_bytes = [0_u8; Self::BYTE_LEN];
        fixed_bytes.copy_from_slice(bytes);
        ProductSymbol::try_from(&fixed_bytes)
    }

    /// Slice of inner 5-bit scheme bytes
    pub fn as_bytes(&self) -> &[u8] {
        self.0.as_slice()
    }

    /// Pack the symbol text into our 5-bit custom scheme
    ///
    /// We pack 5-bit chars instead of ASCII because 6 bytes is the maximum size we can afford
    /// to use symbol in our cryptography without resorting to a one-way hash.
    #[tracing::instrument(level = "trace")]
    pub(crate) fn pack_bytes(
        underlying: UnderlyingSymbol,
        product: Product,
    ) -> [u8; Self::BYTE_LEN] {
        let mut ascii_buf = [0_u8; Self::ASCII_LEN];
        let u_bytes = underlying.trim();
        for i in 0..ascii_buf.len() {
            if i < u_bytes.len() {
                ascii_buf[i] = u_bytes[i];
            } else {
                ascii_buf[i] = 32;
            }
        }
        let (t, params) = product.split();
        ascii_buf[u_bytes.len()] = t as u8;

        let mut symbol_bits: BitVec<Lsb0, u8> = BitVec::new();
        for c in ascii_buf.trim_ascii_end().iter().map(|&b| b as char) {
            let mut is_valid_char = false;
            for (i, sc) in SYMBOL_CHARSET.chars().enumerate() {
                if sc == c {
                    let index = i as u8;
                    // Forcing least significant bit ordering to know where to slice
                    let bits = BitSlice::<Lsb0, u8>::from_element(&index);
                    // Our charset index fits in 5-bit so we only keep the first five
                    // This restricts our charset to max 32 chars (enough for alpha symbols)
                    symbol_bits.extend_from_bitslice(&bits[..5]);
                    is_valid_char = true;
                    break;
                }
            }
            debug_assert!(
                is_valid_char,
                "Illegal char {} charset={}",
                c, SYMBOL_CHARSET
            );
        }
        // Pack concatenated bits into a vector of bytes
        let mut bytes: Vec<u8> = symbol_bits.into_vec();
        debug_assert!(
            bytes.len() <= 4,
            "Expected the symbol to unpack into 4 bytes > 5 * 5 / 8 or less but found {:?} bytes",
            bytes.len()
        );
        bytes.resize(Self::BYTE_LEN, 0_u8);
        let mut fixed_bytes = [0_u8; Self::BYTE_LEN];
        fixed_bytes.copy_from_slice(&bytes);
        if let Some(params) = params {
            fixed_bytes[4] = params as u8;
        }
        fixed_bytes
    }

    /// Decode the symbol fixed bytes by unpacking 5-bit char into ASCII
    pub fn unpack_bytes(fixed_bytes: &[u8; Self::BYTE_LEN]) -> Result<String> {
        // Not sure why we have this
        // if fixed_bytes == &[0_u8; Self::BYTE_LEN] {
        //     return Ok("".to_string());
        // }

        let encoded_bits =
            BitVec::<Lsb0, u8>::from_vec(fixed_bytes[..UnderlyingSymbol::BYTE_LEN].to_vec());
        let mut symbol = String::new();
        // Group into 5-bit chunks each containing an encoded char
        for char_bits_ in encoded_bits.chunks_exact(5) {
            // Resizing our 5-bit encoded char to a byte to compare with our charset
            let mut char_bits = char_bits_.to_bitvec();
            char_bits.resize(8, false);
            let mut is_valid_char = false;
            for (i, c) in SYMBOL_CHARSET.chars().enumerate() {
                let index = i as u8; // Can't non-deterministically fail with our own charset
                let bits = BitSlice::<Lsb0, u8>::from_element(&index);
                if char_bits == bits {
                    // Trimming zero padding chars
                    if i > 0 {
                        symbol.push(c);
                    }
                    is_valid_char = true;
                    break;
                }
            }
            ensure!(
                is_valid_char,
                "Illegal characters packed in {:?} charset={}",
                fixed_bytes,
                SYMBOL_CHARSET
            );
        }
        let mut product_bytes = [0u8; Product::BYTE_LEN];
        product_bytes[0] = symbol.pop().expect("Expected a trailing product char") as u8;
        product_bytes[1..].copy_from_slice(&fixed_bytes[UnderlyingSymbol::BYTE_LEN..]);
        let product = Product::from_fixed_bytes(product_bytes)?;
        Ok(format!("{}{}", symbol, product))
    }
}

impl Tokenizable for ProductSymbol {
    fn from_token(token: Token) -> Result<Self>
    where
        Self: Sized,
    {
        let text = Bytes32::from_token(token)?.to_string();
        text.parse()
    }

    fn into_token(self) -> Token {
        let bytes = Bytes32::from(self);
        bytes.into_token()
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for ProductSymbol {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        let root = UnderlyingSymbol::arbitrary(g);
        ProductSymbol::new(root, Product::Perpetual)
    }
}

impl FromStr for ProductSymbol {
    type Err = Error;

    /// Parse by encoding symbol text into the 5-bit internal representation
    fn from_str(value: &str) -> Result<Self, Self::Err> {
        let (s, p) = ProductSymbol::parse_parts(value)?;
        let bytes = ProductSymbol::pack_bytes(s, p);
        Ok(ProductSymbol(bytes))
    }
}

impl From<ProductSymbol> for UnderlyingSymbol {
    fn from(value: ProductSymbol) -> Self {
        value.split().0
    }
}

// TODO: Restrict usage to development and testing only
impl From<&str> for ProductSymbol {
    fn from(value: &str) -> Self {
        value.parse().unwrap()
    }
}

impl From<String> for ProductSymbol {
    fn from(val: String) -> Self {
        val.as_str().into()
    }
}

impl TryFrom<&[u8; 6]> for ProductSymbol {
    type Error = Error;

    fn try_from(value: &[u8; 6]) -> Result<Self> {
        // Unpack the bytes to ensure they all match the charset
        let _ = ProductSymbol::unpack_bytes(value)?;
        Ok(ProductSymbol(*value))
    }
}

// Also implements `ToString` for free
impl fmt::Display for ProductSymbol {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        // Can't non-deterministically fail to unpack our validated bytes
        write!(f, "{}", ProductSymbol::unpack_bytes(&self.0).unwrap())
    }
}

impl fmt::Debug for ProductSymbol {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_tuple("ProductSymbol")
            .field(&self.to_string())
            .finish()
    }
}

impl From<ProductSymbol> for Bytes32 {
    fn from(value: ProductSymbol) -> Self {
        // Delegate the conversion to the string type
        // Can't fail because we know that the length fits in 32 bytes
        value.to_string().parse().unwrap()
    }
}

#[cfg(feature = "database")]
impl ToSql for ProductSymbol {
    fn to_sql(
        &self,
        ty: &Type,
        out: &mut bytes::BytesMut,
    ) -> Result<IsNull, Box<dyn std::error::Error + 'static + Sync + Send>> {
        self.to_string().to_sql(ty, out)
    }

    fn accepts(ty: &Type) -> bool {
        <String as ToSql>::accepts(ty)
    }

    to_sql_checked!();
}

#[cfg(feature = "database")]
impl<'a> FromSql<'a> for ProductSymbol {
    fn from_sql(
        ty: &Type,
        raw: &'a [u8],
    ) -> Result<Self, Box<dyn std::error::Error + Sync + Send>> {
        let decoded_string = String::from_sql(ty, raw)?;
        let symbol: ProductSymbol = decoded_string.as_str().into();
        Ok(symbol)
    }

    fn accepts(ty: &Type) -> bool {
        <String as FromSql>::accepts(ty)
    }
}

#[cfg_attr(feature = "python", pyclass(frozen))]
#[derive(
    Debug, Copy, Clone, PartialEq, Deserialize, Serialize, std::hash::Hash, AbiToken, Eq, Default,
)]
pub enum OrderSide {
    #[default]
    Bid,
    Ask,
}

#[cfg(feature = "python")]
impl FromStr for OrderSide {
    type Err = Error;
    fn from_str(s: &str) -> Result<Self> {
        match s {
            "Bid" => Ok(OrderSide::Bid),
            "Ask" => Ok(OrderSide::Ask),
            _ => Err(Error::Parse(format!("Invalid order side: {}", s))),
        }
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for OrderSide {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        let discriminator = g.choose(&[0, 1]).unwrap();
        match discriminator {
            0 => OrderSide::Bid,
            1 => OrderSide::Ask,
            _ => panic!("invalid discriminator"),
        }
    }
}

impl OrderSide {
    pub fn reverse(&self) -> &OrderSide {
        match *self {
            OrderSide::Bid => &OrderSide::Ask,
            OrderSide::Ask => &OrderSide::Bid,
        }
    }
}

impl From<OrderSide> for i32 {
    fn from(order_side: OrderSide) -> Self {
        order_side as i32
    }
}

// All short enums codes are u8 to ensure that we can use only 1 byte in binary encoding
impl From<OrderSide> for u8 {
    fn from(value: OrderSide) -> Self {
        match value {
            OrderSide::Bid => 0,
            OrderSide::Ask => 1,
        }
    }
}

// All short enums codes are u8 to ensure that we can use only 1 byte in binary encoding
impl From<&OrderSide> for u8 {
    fn from(value: &OrderSide) -> Self {
        match value {
            OrderSide::Bid => 0,
            OrderSide::Ask => 1,
        }
    }
}

impl TryFrom<u8> for OrderSide {
    type Error = Error;

    fn try_from(value: u8) -> Result<Self, Self::Error> {
        Ok(match value {
            0 => OrderSide::Bid,
            1 => OrderSide::Ask,
            _ => bail!("Invalid order type code {:?}", value),
        })
    }
}

impl TryFrom<i32> for OrderSide {
    type Error = Error;

    fn try_from(value: i32) -> Result<Self, Self::Error> {
        let byte: u8 = value.try_into()?;
        byte.try_into()
    }
}

#[cfg(feature = "database")]
impl<'a> FromSql<'a> for OrderSide {
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

#[cfg(feature = "database")]
impl ToSql for OrderSide {
    fn to_sql(
        &self,
        ty: &Type,
        out: &mut bytes::BytesMut,
    ) -> Result<IsNull, Box<dyn std::error::Error + 'static + Sync + Send>> {
        let value: i32 = (*self).into();
        value.to_sql(ty, out)
    }

    fn accepts(ty: &Type) -> bool {
        <i32 as ToSql>::accepts(ty)
    }

    to_sql_checked!();
}

/// Holds a URL string valid for a node
#[derive(Debug, Default, Clone, Eq, PartialEq, std::hash::Hash, Serialize)]
pub struct NodeUrl(pub String);

impl NodeUrl {
    fn new(url: String) -> Result<Self> {
        if URL_RE.is_match(&url) {
            Ok(NodeUrl(url))
        } else {
            Err(Error::Parse(format!("Invalid URL: {}", url)))
        }
    }

    #[cfg(feature = "test_harness")]
    pub fn with_localhost(port: u16) -> Self {
        NodeUrl(format!(
            "http://{}:{}",
            crate::constants::LOCALHOST_ADDRESS,
            port
        ))
    }

    /// Creates a service URL by convention for the given node ID
    pub fn with_service(node_id: u64) -> Self {
        NodeUrl(format!("http://operator-node{}:8080", node_id))
    }
}

impl FromStr for NodeUrl {
    type Err = Error;

    fn from_str(s: &str) -> Result<Self> {
        NodeUrl::new(s.to_string())
    }
}

impl<'de> Deserialize<'de> for NodeUrl {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        let url = String::deserialize(deserializer)?;
        NodeUrl::new(url).map_err(serde::de::Error::custom)
    }
}

impl fmt::Display for NodeUrl {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

/// Verified state relative time value in seconds with a wall clock timestamp.
#[cfg_attr(feature = "python", pyclass(name = "AdvanceTime", frozen, get_all))]
#[derive(Debug, Default, Clone, Copy, PartialEq, Serialize, Deserialize, AbiToken, AsKeccak256)]
pub struct StampedTimeValue {
    pub value: TimeValue,
    pub timestamp: i64,
}

#[cfg(feature = "python")]
#[pymethods]
impl StampedTimeValue {
    #[new]
    fn new_py(value: TimeValue, timestamp: i64) -> Self {
        Self { value, timestamp }
    }
}

impl StampedTimeValue {
    pub fn with_now_timestamp(value: TimeValue) -> Self {
        Self {
            value,
            timestamp: DateTime::<Utc>::from(SystemTime::now()).timestamp_millis(),
        }
    }
}

impl std::fmt::Display for StampedTimeValue {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for StampedTimeValue {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        Self {
            value: u64::arbitrary(g),
            timestamp: i64::arbitrary(g),
        }
    }
}

#[cfg(feature = "arbitrary")]
fn arbitrary_h256(g: &mut quickcheck::Gen) -> EthH256 {
    let vec: Vec<u8> = (0..256 / 8).map(|_| u8::arbitrary(g)).collect();
    let arr: [u8; 256 / 8] = std::convert::TryInto::try_into(vec).unwrap();
    EthH256::from_slice(&arr)
}

/// Signed integer adapter
#[derive(Debug, Clone, Copy, Default, PartialEq, Deserialize, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct I128 {
    pub negative_sign: bool,
    #[serde(with = "as_scaled_fraction")]
    pub abs: U128,
}

impl Tokenizable for I128 {
    fn from_token(token: Token) -> Result<Self>
    where
        Self: Sized,
    {
        let num = Token::into_uint(token).ok_or_else(|| error!("Token must convert into U256"))?;
        let num_bytes: [u8; 32] = num.into();
        let negative_sign = num_bytes[15] == 1_u8;
        let mut abs_bytes = [0_u8; 16];
        abs_bytes.copy_from_slice(&num_bytes[16..]);
        let abs = U128::from(abs_bytes);
        Ok(I128 { negative_sign, abs })
    }

    fn into_token(self) -> Token {
        let mut num_slice = vec![];
        // We use byte index 15 (first before value) for the boolean sign
        let mut sign_bytes = [0_u8; 16];
        if self.negative_sign {
            sign_bytes[15] = 1_u8;
        }
        num_slice.extend_from_slice(sign_bytes.as_slice());
        let abs: [u8; 16] = self.abs.into();
        num_slice.extend_from_slice(abs.as_slice());
        let mut num_bytes = [0_u8; 32];
        num_bytes.copy_from_slice(&num_slice);
        let num = U256::from(num_bytes);
        num.into_token()
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for I128 {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        Self {
            negative_sign: bool::arbitrary(g),
            abs: u128::arbitrary(g).into(),
        }
    }
}

/// Common interface for newTypes wrapping fixed bytes like structures
///
/// This trait offers a consistent way to access inner bytes of our abstract types.
pub trait FixedBytesWrapper {
    type FixedBytes;

    /// Tries to copy the given slice into the inner type
    fn copy_fixed_bytes(bytes: &[u8]) -> Result<Self::FixedBytes>;

    /// Makes an instance from the given slice
    fn from_slice(bytes: &[u8]) -> Self;

    /// Tries to make an instance from the given slice
    fn try_from_slice(bytes: &[u8]) -> Result<Self>
    where
        Self: Sized;

    /// Returns the inner data as a byte array slice
    fn as_bytes(&self) -> &[u8];
}

// TODO: Either use this Hash adapter everywhere except internally when interfacing with either Ethereum or the SMT
// Or, fork the SMT to standardize both H256 into a single system-wide structure, then remove this adapter.
#[derive(
    Debug,
    Clone,
    Copy,
    Default,
    PartialEq,
    Eq,
    std::hash::Hash,
    PartialOrd,
    Ord,
    Deserialize,
    Serialize,
    AbiToken,
    AsKeccak256,
)]
pub struct Hash(EthH256);

#[cfg(feature = "python")]
impl FromPyObject<'_> for Hash {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let hex = ob.extract::<String>()?;
        Ok(Self(EthH256::from_str(&hex).map_err(|e| {
            crate::types::state::exported::python::DdxCommonError::new_err(e.to_string())
        })?))
    }
}

#[cfg(feature = "python")]
impl IntoPy<PyObject> for Hash {
    fn into_py(self, py: Python) -> PyObject {
        format!("{}", self).into_py(py)
    }
}

impl FixedBytesWrapper for Hash {
    type FixedBytes = EthH256;

    fn copy_fixed_bytes(bytes: &[u8]) -> Result<Self::FixedBytes> {
        // Wraps the same structure as `Bytes32`
        Bytes32::copy_fixed_bytes(bytes)
    }

    fn from_slice(bytes: &[u8]) -> Self {
        Hash::copy_fixed_bytes(bytes).unwrap().into()
    }

    fn try_from_slice(bytes: &[u8]) -> Result<Self> {
        Ok(Hash::copy_fixed_bytes(bytes)?.into())
    }

    fn as_bytes(&self) -> &[u8] {
        self.0.as_bytes()
    }
}

impl fmt::Display for Hash {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "0x{}", self.as_bytes().to_hex::<String>())
    }
}

impl From<U256> for Hash {
    fn from(value: U256) -> Self {
        let mut bytes = vec![0_u8; KECCAK256_DIGEST_SIZE];
        value.to_big_endian(&mut bytes);
        Hash::from_slice(&bytes)
    }
}

impl From<Hash> for U256 {
    fn from(value: Hash) -> Self {
        U256::from_big_endian(value.as_bytes())
    }
}

impl From<Bytes32> for Hash {
    fn from(value: Bytes32) -> Self {
        Hash(value.0)
    }
}

#[cfg(feature = "arbitrary")]
fn arbitrary_h520(g: &mut quickcheck::Gen) -> H520 {
    const BYTE_LEN: usize = size_of::<H520>();
    let vec: Vec<u8> = (0..BYTE_LEN).map(|_| u8::arbitrary(g)).collect();
    let arr: [u8; BYTE_LEN] = std::convert::TryInto::try_into(vec).unwrap();
    let mut fixed_bytes = [0_u8; BYTE_LEN];
    fixed_bytes.copy_from_slice(&arr);
    H520(fixed_bytes)
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for Hash {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        Self(arbitrary_h256(g))
    }
}

impl FromStr for Hash {
    type Err = <EthH256 as FromStr>::Err;

    fn from_str(text: &str) -> Result<Self, Self::Err> {
        let hash = EthH256::from_str(text)?;
        Ok(Hash(hash))
    }
}

impl From<H256> for Hash {
    fn from(value: H256) -> Self {
        let bytes: [u8; 32] = value.into();
        Hash(crate::ethereum_types::H256(bytes))
    }
}

impl From<Hash> for H256 {
    fn from(value: Hash) -> Self {
        let bytes: [u8; 32] = value.into();
        bytes.into()
    }
}

// Conversion from refs is reasonable for trivial byte copying
impl<T: Copy + Into<Hash>> From<&T> for Hash {
    fn from(value: &T) -> Self {
        (*value).into()
    }
}

impl From<[u8; 32]> for Hash {
    fn from(value: [u8; 32]) -> Self {
        Hash(EthH256(value))
    }
}

impl From<EthH256> for Hash {
    fn from(value: EthH256) -> Self {
        Hash(value)
    }
}

impl From<Hash> for EthH256 {
    fn from(value: Hash) -> Self {
        value.0
    }
}

impl From<Hash> for [u8; 32] {
    fn from(value: Hash) -> Self {
        value.0.to_fixed_bytes()
    }
}

impl From<u32> for Hash {
    fn from(value: u32) -> Self {
        Bytes32::from(value as u64).into()
    }
}

impl fmt::LowerHex for Hash {
    /// #Examples
    ///
    /// ```
    /// use ddx_common::types::primitives::Hash;
    /// let x = Hash::from([1; 32]);
    /// assert_eq!(
    ///     format!("{:#x}", x),
    ///     "0x0101010101010101010101010101010101010101010101010101010101010101"
    /// );
    /// ```
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let val = self.0;

        fmt::LowerHex::fmt(&val, f) // delegate to EthH256 implementation
    }
}

#[derive(
    Debug,
    Clone,
    Copy,
    Default,
    std::hash::Hash,
    PartialEq,
    Eq,
    Serialize,
    Deserialize,
    PartialOrd,
    Ord,
)]
pub struct Bytes25(#[serde(with = "as_bytes25_hex")] [u8; 25]);

impl Bytes25 {
    pub const BYTE_LEN: usize = size_of::<Self>();
}

#[cfg(feature = "python")]
impl FromPyObject<'_> for Bytes25 {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let text = ob.extract::<String>()?;
        Ok(from_hex(text).and_then(|v| Bytes25::try_from_slice(&v))?)
    }
}

#[cfg(feature = "python")]
impl IntoPy<PyObject> for Bytes25 {
    fn into_py(self, py: Python) -> PyObject {
        self.hex().into_py(py)
    }
}

impl Bytes25 {
    pub(crate) fn hex(&self) -> String {
        format!("0x{}", self.as_bytes().to_hex::<String>())
    }
}

impl FixedBytesWrapper for Bytes25 {
    type FixedBytes = [u8; Self::BYTE_LEN];

    fn copy_fixed_bytes(bytes: &[u8]) -> Result<Self::FixedBytes> {
        ensure!(bytes.len() == Self::BYTE_LEN, "Expected exactly 25 bytes");
        let mut fixed_bytes = [0_u8; Self::BYTE_LEN];
        fixed_bytes.copy_from_slice(bytes);
        Ok(fixed_bytes)
    }

    fn from_slice(bytes: &[u8]) -> Self {
        Bytes25(Bytes25::copy_fixed_bytes(bytes).unwrap())
    }

    fn try_from_slice(bytes: &[u8]) -> Result<Self> {
        Ok(Bytes25(Bytes25::copy_fixed_bytes(bytes)?))
    }

    fn as_bytes(&self) -> &[u8] {
        self.0.as_slice()
    }
}

impl From<Hash> for Bytes25 {
    fn from(value: Hash) -> Self {
        let fixed_bytes = value.0.as_fixed_bytes();
        Bytes25::from_slice(&fixed_bytes[..Self::BYTE_LEN])
    }
}

impl<T: Into<Bytes25> + Copy> From<&T> for Bytes25 {
    fn from(value: &T) -> Self {
        (*value).into()
    }
}

impl Tokenizable for Bytes25 {
    fn from_token(token: Token) -> Result<Self>
    where
        Self: Sized,
    {
        let token_bytes32: Bytes32 = Bytes32::from_token(token)?;
        Ok(Bytes25::from_slice(
            &token_bytes32.as_bytes()[..Self::BYTE_LEN],
        ))
    }

    fn into_token(self) -> Token {
        let mut bytes = self.0.to_vec();
        bytes.resize(32, 0_u8);
        let mut fixed_bytes = [0_u8; Bytes32::BYTE_LEN];
        fixed_bytes.copy_from_slice(&bytes);
        let bytes32: Bytes32 = fixed_bytes.into();
        bytes32.into_token()
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for Bytes25 {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        let hash = arbitrary_h256(g);
        let fixed_bytes = hash.as_fixed_bytes();
        Bytes25::from_slice(&fixed_bytes[..25])
    }
}

pub type CompressedKey = Bytes33;

#[derive(
    Debug, Clone, Copy, std::hash::Hash, PartialEq, Eq, Serialize, Deserialize, PartialOrd, Ord,
)]
pub struct Bytes33(#[serde(with = "as_bytes33_hex")] [u8; 33]);

impl Bytes33 {
    pub const BYTE_LEN: usize = size_of::<Self>();
}

impl FixedBytesWrapper for Bytes33 {
    type FixedBytes = [u8; Self::BYTE_LEN];

    fn copy_fixed_bytes(bytes: &[u8]) -> Result<Self::FixedBytes> {
        ensure!(bytes.len() == 33, "Expected exactly 33 bytes");
        let mut fixed_bytes = [0_u8; Self::BYTE_LEN];
        fixed_bytes.copy_from_slice(bytes);
        Ok(fixed_bytes)
    }

    fn from_slice(bytes: &[u8]) -> Self {
        Bytes33(Bytes33::copy_fixed_bytes(bytes).unwrap())
    }

    fn try_from_slice(bytes: &[u8]) -> Result<Self> {
        Ok(Bytes33(Bytes33::copy_fixed_bytes(bytes)?))
    }

    fn as_bytes(&self) -> &[u8] {
        self.0.as_slice()
    }
}

impl<T: Into<Bytes33> + Copy> From<&T> for Bytes33 {
    fn from(value: &T) -> Self {
        (*value).into()
    }
}

impl From<Bytes33> for [u8; Bytes33::BYTE_LEN] {
    fn from(value: Bytes33) -> Self {
        value.0
    }
}

impl Tokenizable for Bytes33 {
    fn from_token(token: Token) -> Result<Self>
    where
        Self: Sized,
    {
        let bytes = token
            .into_fixed_bytes()
            .ok_or_else(|| error!("Expected fixed bytes in token"))?;
        Ok(Bytes33(Bytes33::copy_fixed_bytes(&bytes)?))
    }

    fn into_token(self) -> Token {
        Token::FixedBytes(self.as_bytes().to_vec())
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for Bytes33 {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        let h = arbitrary_h256(g);
        let mut bytes = h.as_bytes().to_vec();
        bytes.resize(Self::BYTE_LEN, 0_u8);
        Bytes33::from_slice(&bytes)
    }
}

#[derive(Debug, Clone, Default, Copy, std::hash::Hash, PartialEq, Eq, PartialOrd, Ord)]
pub struct Bytes4([u8; 4]);

impl Bytes4 {
    pub const BYTE_LEN: usize = size_of::<Self>();
}

/// Abbreviates the `Hash` by copying its first four bytes
impl From<Hash> for Bytes4 {
    fn from(h: Hash) -> Self {
        let mut fb = [0_u8; Self::BYTE_LEN];
        fb.copy_from_slice(&h.as_bytes()[..Self::BYTE_LEN]);
        Bytes4(fb)
    }
}

impl From<Bytes25> for Bytes4 {
    fn from(b: Bytes25) -> Self {
        let mut fb = [0_u8; Self::BYTE_LEN];
        fb.copy_from_slice(&b.as_bytes()[..Self::BYTE_LEN]);
        Bytes4(fb)
    }
}

impl From<Bytes4> for [u8; Bytes4::BYTE_LEN] {
    fn from(value: Bytes4) -> Self {
        value.0
    }
}

impl From<[u8; Bytes4::BYTE_LEN]> for Bytes4 {
    fn from(value: [u8; Bytes4::BYTE_LEN]) -> Self {
        Bytes4(value)
    }
}

impl FixedBytesWrapper for Bytes4 {
    type FixedBytes = [u8; Self::BYTE_LEN];

    fn copy_fixed_bytes(bytes: &[u8]) -> Result<Self::FixedBytes> {
        ensure!(bytes.len() == Self::BYTE_LEN, "Expected exactly 4 bytes");
        let mut fixed_bytes = [0_u8; Self::BYTE_LEN];
        fixed_bytes.copy_from_slice(bytes);
        Ok(fixed_bytes)
    }

    fn from_slice(bytes: &[u8]) -> Self {
        Bytes4(Bytes4::copy_fixed_bytes(bytes).unwrap())
    }

    fn try_from_slice(bytes: &[u8]) -> Result<Self> {
        Ok(Bytes4(Bytes4::copy_fixed_bytes(bytes)?))
    }

    fn as_bytes(&self) -> &[u8] {
        self.0.as_slice()
    }
}

impl Tokenizable for Bytes4 {
    fn from_token(token: Token) -> Result<Self>
    where
        Self: Sized,
    {
        let bytes = token
            .into_fixed_bytes()
            .ok_or_else(|| error!("Expected fixed bytes in token"))?;
        Ok(Bytes4(Bytes4::copy_fixed_bytes(&bytes)?))
    }

    fn into_token(self) -> Token {
        Token::FixedBytes(self.as_bytes().to_vec())
    }
}

// TODO: Use a macro_rules for all these Bytes impl
#[derive(
    Clone, Default, Copy, std::hash::Hash, PartialEq, Eq, Serialize, Deserialize, PartialOrd, Ord,
)]
pub struct Bytes21(#[serde(with = "as_address_hex")] [u8; 21]);

impl Bytes21 {
    pub const BYTE_LEN: usize = size_of::<Self>();
}

#[cfg(feature = "python")]
impl FromPyObject<'_> for Bytes21 {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let value = ob.extract::<String>()?;
        Ok(from_hex(value).and_then(|v| Bytes21::try_from_slice(&v))?)
    }
}

#[cfg(feature = "python")]
impl ToPyObject for Bytes21 {
    fn to_object(&self, py: Python) -> PyObject {
        self.hex().to_object(py)
    }
}

#[cfg(feature = "python")]
impl IntoPy<PyObject> for Bytes21 {
    fn into_py(self, py: Python) -> PyObject {
        self.to_object(py)
    }
}

impl Bytes21 {
    pub fn to_eth_address(&self) -> Address {
        Address::from_slice(&self.as_bytes()[1..])
    }

    /// From normal 0x prefixed Ethereum address injecting the chain id.
    pub fn parse_eth_address(value: &str) -> Result<Self> {
        let result: Address = serde_json::from_str(format!(r#""{}""#, value).as_str())?;
        Ok(result.into())
    }

    #[cfg(any(feature = "python", feature = "test_harness"))]
    pub fn hex(&self) -> String {
        format!("0x{}", self.as_bytes().to_hex::<String>())
    }
}

impl FixedBytesWrapper for Bytes21 {
    type FixedBytes = [u8; Self::BYTE_LEN];

    fn copy_fixed_bytes(bytes: &[u8]) -> Result<Self::FixedBytes> {
        ensure!(bytes.len() == Self::BYTE_LEN, "Expected exactly 21 bytes");
        let mut fixed_bytes = [0_u8; Self::BYTE_LEN];
        fixed_bytes.copy_from_slice(bytes);
        Ok(fixed_bytes)
    }

    fn from_slice(bytes: &[u8]) -> Self {
        Bytes21(Bytes21::copy_fixed_bytes(bytes).unwrap())
    }

    fn try_from_slice(bytes: &[u8]) -> Result<Self> {
        Ok(Bytes21(Bytes21::copy_fixed_bytes(bytes)?))
    }

    fn as_bytes(&self) -> &[u8] {
        self.0.as_slice()
    }
}

impl<T: Into<Bytes21> + Copy> From<&T> for Bytes21 {
    fn from(value: &T) -> Self {
        (*value).into()
    }
}

impl Tokenizable for Bytes21 {
    fn from_token(token: Token) -> Result<Self>
    where
        Self: Sized,
    {
        let bytes = token
            .into_fixed_bytes()
            .ok_or_else(|| error!("Expected fixed bytes in token"))?;
        Ok(Bytes21(Bytes21::copy_fixed_bytes(&bytes)?))
    }

    fn into_token(self) -> Token {
        Token::FixedBytes(self.as_bytes().to_vec())
    }
}

impl From<Address> for Bytes21 {
    /// From Ethereum address injecting the chain id.
    fn from(value: Address) -> Self {
        let mut bytes = vec![CHAIN_ETHEREUM];
        bytes.extend_from_slice(value.as_bytes());
        Bytes21::from_slice(&bytes)
    }
}

impl From<u16> for Bytes21 {
    fn from(value: u16) -> Self {
        Address::from_low_u64_be(value as u64).into()
    }
}

impl From<Bytes21> for [u8; size_of::<Bytes21>()] {
    fn from(val: Bytes21) -> Self {
        val.0
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for Bytes21 {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        let h = arbitrary_h160(g);
        let mut bytes = vec![0_u8];
        bytes.extend_from_slice(h.as_bytes());
        Bytes21::from_slice(&bytes)
    }
}

#[cfg(feature = "database")]
impl ToSql for Bytes21 {
    fn to_sql(
        &self,
        ty: &Type,
        out: &mut bytes::BytesMut,
    ) -> Result<IsNull, Box<dyn std::error::Error + 'static + Sync + Send>> {
        self.as_bytes().to_sql(ty, out)
    }

    fn accepts(ty: &Type) -> bool {
        <&[u8] as ToSql>::accepts(ty)
    }

    to_sql_checked!();
}

#[cfg(feature = "database")]
impl<'a> FromSql<'a> for Bytes21 {
    fn from_sql(
        ty: &Type,
        raw: &'a [u8],
    ) -> Result<Self, Box<dyn std::error::Error + Sync + Send>> {
        let decoded_bytes: &[u8] = <&[u8]>::from_sql(ty, raw)?;
        let bytes: Self = Self::from_slice(decoded_bytes);
        Ok(bytes)
    }

    fn accepts(ty: &Type) -> bool {
        <&[u8] as FromSql>::accepts(ty)
    }
}

#[derive(
    Debug,
    Clone,
    Copy,
    Default,
    std::hash::Hash,
    PartialEq,
    Eq,
    PartialOrd,
    Ord,
    Serialize,
    Deserialize,
    AbiToken,
)]
#[serde(transparent)]
pub struct Bytes32(EthH256);

#[cfg(feature = "python")]
impl FromPyObject<'_> for Bytes32 {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let hex = ob.extract::<String>()?;
        Ok(Self(EthH256::from_str(&hex).map_err(|e| {
            crate::types::state::exported::python::DdxCommonError::new_err(e.to_string())
        })?))
    }
}

impl Bytes32 {
    pub const BYTE_LEN: usize = size_of::<Self>();
}

impl FixedBytesWrapper for Bytes32 {
    type FixedBytes = EthH256;

    fn copy_fixed_bytes(bytes: &[u8]) -> Result<Self::FixedBytes> {
        ensure!(bytes.len() == Self::BYTE_LEN, "Expected exactly 32 bytes");
        let mut fixed_bytes: [u8; Self::BYTE_LEN] = [0; Self::BYTE_LEN];
        fixed_bytes.copy_from_slice(bytes);
        Ok(EthH256(fixed_bytes))
    }

    fn from_slice(bytes: &[u8]) -> Self {
        Bytes32(Bytes32::copy_fixed_bytes(bytes).unwrap())
    }

    fn try_from_slice(bytes: &[u8]) -> Result<Self> {
        Ok(Bytes32(Bytes32::copy_fixed_bytes(bytes)?))
    }

    fn as_bytes(&self) -> &[u8] {
        self.0.as_bytes()
    }
}

impl From<u64> for Bytes32 {
    /// Converts from the big endian bytes of `u64`
    fn from(value: u64) -> Self {
        EthH256::from_low_u64_be(value).into()
    }
}

impl From<Address> for Bytes32 {
    fn from(value: Address) -> Self {
        Bytes32(EthH256::from(value))
    }
}

impl FromStr for Bytes32 {
    type Err = Error;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        let str_bytes = value.as_bytes();
        let str_len = str_bytes.len();
        ensure!(
            str_len < Self::BYTE_LEN,
            "Bytes32 has 31 utf8 bytes prefixed with 1 length byte"
        );
        // First byte is the string length
        let mut bytes = [0u8; Self::BYTE_LEN];
        bytes[0] = str_len as u8;
        bytes[1..str_len + 1].copy_from_slice(str_bytes);
        Ok(Bytes32::from_slice(&bytes))
    }
}

// Also implements `ToString` for free
impl fmt::Display for Bytes32 {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        let mut bytes = self.as_bytes().to_vec();
        // First byte is the string length
        let length = bytes.remove(0);
        bytes.truncate(length as usize);
        write!(f, "{}", String::from_utf8_lossy(&bytes))
    }
}

impl From<Bytes32> for EthH256 {
    fn from(value: Bytes32) -> Self {
        value.0
    }
}

impl From<Bytes32> for [u8; Bytes32::BYTE_LEN] {
    fn from(value: Bytes32) -> Self {
        value.0.to_fixed_bytes()
    }
}

impl From<[u8; Bytes32::BYTE_LEN]> for Bytes32 {
    fn from(value: [u8; 32]) -> Self {
        Bytes32(EthH256(value))
    }
}

impl From<EthH256> for Bytes32 {
    fn from(value: EthH256) -> Self {
        Bytes32(value)
    }
}

impl From<Bytes25> for Bytes32 {
    fn from(value: Bytes25) -> Self {
        let mut bytes = [0_u8; Self::BYTE_LEN];
        bytes[0..25].copy_from_slice(value.as_bytes());
        Bytes32(EthH256(bytes))
    }
}

#[derive(Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct Signature(#[serde(with = "as_bytes65_hex")] [u8; 65]);

#[cfg(feature = "python")]
impl FromPyObject<'_> for Signature {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let str_repr = ob.extract::<String>()?;
        Ok(Self::from_str(&str_repr)?)
    }
}

#[cfg(feature = "python")]
impl IntoPy<PyObject> for Signature {
    fn into_py(self, py: Python) -> PyObject {
        self.to_string().into_py(py)
    }
}

impl Signature {
    pub const BYTE_LEN: usize = size_of::<Self>();

    pub fn new(fixed_bytes: [u8; Self::BYTE_LEN]) -> Self {
        Signature(fixed_bytes)
    }

    /// Convert to vrs format, the recovery id is encoded in the first byte
    pub fn as_vrs(&self) -> H520 {
        let rsv_slice = self.as_bytes();
        let mut vrs_bytes: Vec<u8> = Vec::with_capacity(Self::BYTE_LEN);
        vrs_bytes.push(rsv_slice[64]);
        vrs_bytes.extend_from_slice(&rsv_slice[..Self::BYTE_LEN - 1]);
        H520::from_slice(&vrs_bytes)
    }

    /// Convert from vrs format, the recovery id is encoded in the first byte
    pub fn from_vrs(vrs: H520) -> Self {
        let mut bytes = [0u8; Self::BYTE_LEN];
        bytes[..Self::BYTE_LEN - 1].copy_from_slice(&vrs[1..]);
        bytes[Self::BYTE_LEN - 1] = vrs.as_bytes()[0];
        Signature(bytes)
    }

    /// Convert from parts of r, s, v
    pub fn from_parts(r: &[u8], s: &[u8], v: u8) -> Self {
        let mut bytes = [0u8; Self::BYTE_LEN];
        bytes[..r.len()].copy_from_slice(r);
        bytes[r.len()..r.len() + s.len()].copy_from_slice(s);
        bytes[Self::BYTE_LEN - 1] = v;
        Signature(bytes)
    }

    fn serialize(&self) -> String {
        format!("0x{}", self.as_bytes().to_hex::<String>())
    }
}

impl fmt::Debug for Signature {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_tuple("Signature").field(&self.serialize()).finish()
    }
}

impl fmt::Display for Signature {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.serialize())
    }
}

impl FixedBytesWrapper for Signature {
    type FixedBytes = [u8; Self::BYTE_LEN];

    fn copy_fixed_bytes(bytes: &[u8]) -> Result<Self::FixedBytes> {
        ensure!(bytes.len() == Self::BYTE_LEN, "Expected exactly 65 bytes");
        let mut fixed_bytes = [0_u8; Self::BYTE_LEN];
        fixed_bytes.copy_from_slice(bytes);
        Ok(fixed_bytes)
    }

    fn from_slice(bytes: &[u8]) -> Self {
        Signature(Signature::copy_fixed_bytes(bytes).unwrap())
    }

    fn try_from_slice(bytes: &[u8]) -> Result<Self> {
        Ok(Signature(Signature::copy_fixed_bytes(bytes)?))
    }

    fn as_bytes(&self) -> &[u8] {
        self.0.as_slice()
    }
}

impl Default for Signature {
    fn default() -> Self {
        Signature([0; Self::BYTE_LEN])
    }
}

impl From<Signature> for H520 {
    fn from(value: Signature) -> Self {
        H520(value.0)
    }
}

impl From<H520> for Signature {
    fn from(value: H520) -> Self {
        Signature(value.0)
    }
}

impl From<Signature> for [u8; Signature::BYTE_LEN] {
    fn from(value: Signature) -> Self {
        value.0
    }
}

impl FromStr for Signature {
    type Err = Error;

    /// Parse by encoding symbol text into the 5-bit internal representation
    fn from_str(value: &str) -> Result<Self, Self::Err> {
        Ok(Signature::from_slice(&from_hex(value)?))
    }
}

impl From<&str> for Signature {
    fn from(value: &str) -> Self {
        value.parse().unwrap()
    }
}

impl From<String> for Signature {
    fn from(val: String) -> Self {
        val.as_str().into()
    }
}

// TODO: Do we ever want to tokenize the signature as an rsv value? All
// of our smart contracts are using vrs, so this seems less useful than
// the alternative.
impl Tokenizable for Signature {
    fn from_token(token: Token) -> Result<Self>
    where
        Self: Sized,
    {
        let bytes = token
            .into_fixed_bytes()
            .ok_or_else(|| error!("Expected fixed bytes in token"))?;
        Ok(Signature(Signature::copy_fixed_bytes(&bytes)?))
    }

    fn into_token(self) -> Token {
        Token::FixedBytes(self.as_bytes().to_vec())
    }
}

#[cfg(feature = "arbitrary")]
impl Arbitrary for Signature {
    fn arbitrary(g: &mut quickcheck::Gen) -> Self {
        arbitrary_h520(g).into()
    }
}

// This section contains SQL conversion implementations

#[cfg(feature = "database")]
impl ToSql for Hash {
    fn to_sql(
        &self,
        ty: &Type,
        out: &mut bytes::BytesMut,
    ) -> Result<IsNull, Box<dyn std::error::Error + 'static + Sync + Send>> {
        self.as_bytes().to_sql(ty, out)
    }

    fn accepts(ty: &Type) -> bool {
        <&[u8] as ToSql>::accepts(ty)
    }

    to_sql_checked!();
}

#[cfg(feature = "database")]
impl<'a> FromSql<'a> for Hash {
    fn from_sql(
        ty: &Type,
        raw: &'a [u8],
    ) -> Result<Self, Box<dyn std::error::Error + Sync + Send>> {
        let raw_bytes = Vec::from_sql(ty, raw)?;
        let hash = Hash::try_from_slice(&raw_bytes)?;
        Ok(hash)
    }

    fn accepts(ty: &Type) -> bool {
        <Vec<u8> as FromSql>::accepts(ty)
    }
}

#[cfg(feature = "database")]
impl ToSql for Bytes25 {
    fn to_sql(
        &self,
        ty: &Type,
        out: &mut bytes::BytesMut,
    ) -> Result<IsNull, Box<dyn std::error::Error + 'static + Sync + Send>> {
        self.0.to_vec().to_sql(ty, out)
    }

    fn accepts(ty: &Type) -> bool {
        <Vec<u8> as ToSql>::accepts(ty)
    }

    to_sql_checked!();
}

#[cfg(feature = "database")]
impl<'a> FromSql<'a> for Bytes25 {
    fn from_sql(
        ty: &Type,
        raw: &'a [u8],
    ) -> Result<Self, Box<dyn std::error::Error + Sync + Send>> {
        let bytes: Vec<u8> = Vec::from_sql(ty, raw)?;
        let fixed_bytes = Bytes25::copy_fixed_bytes(&bytes)?;
        Ok(Bytes25(fixed_bytes))
    }

    fn accepts(ty: &Type) -> bool {
        <Vec<u8> as FromSql>::accepts(ty)
    }
}

#[cfg(feature = "database")]
impl ToSql for Signature {
    fn to_sql(
        &self,
        ty: &Type,
        out: &mut bytes::BytesMut,
    ) -> Result<IsNull, Box<dyn std::error::Error + 'static + Sync + Send>> {
        self.0.to_vec().to_sql(ty, out)
    }

    fn accepts(ty: &Type) -> bool {
        <&[u8] as ToSql>::accepts(ty)
    }

    to_sql_checked!();
}

#[cfg(feature = "database")]
impl<'a> FromSql<'a> for Signature {
    fn from_sql(
        ty: &Type,
        raw: &'a [u8],
    ) -> Result<Self, Box<dyn std::error::Error + Sync + Send>> {
        let bytes: Vec<u8> = Vec::from_sql(ty, raw)?;
        Ok(Signature::from_slice(&bytes))
    }

    fn accepts(ty: &Type) -> bool {
        <Vec<u8> as FromSql>::accepts(ty)
    }
}

pub type SessionSignature = Option<Signature>;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bytes32_str_conversion() {
        let text = "TEST".to_string();
        let bytes: Bytes32 = text.parse().unwrap();
        let text2 = bytes.to_string();
        assert_eq!(text, text2);
    }

    #[test]
    fn test_default_enclave_signature() {
        let sig: Signature = Default::default();
        let value = serde_json::to_value(sig).unwrap();
        tracing::debug!("The encoded value {:?}", value);
        let _sig2: Signature = serde_json::from_value(value).unwrap();
    }

    #[test]
    fn test_node_url() {
        let _ = "http://localhost:8080".parse::<NodeUrl>().unwrap();
        let _ = "http://127.0.0.1:8080".parse::<NodeUrl>().unwrap();
        let _ = "https://127.0.0.1:8080".parse::<NodeUrl>().unwrap();
        let _ = "https://127.0.0.1:8080/foo".parse::<NodeUrl>().unwrap();
        let _ = "http://localhost:8080/foo".parse::<NodeUrl>().unwrap();
        let _ = "http://localhost:8080/foo/bar".parse::<NodeUrl>().unwrap();
        assert!("foo".parse::<NodeUrl>().is_err());
        assert!("tcp://localhost:8080/foo/bar".parse::<NodeUrl>().is_err());
        // IPv6 not tested so not supported yet
        assert!(
            "http://2345:0425:2CA1:0000:0000:0567:5673:23b5"
                .parse::<NodeUrl>()
                .is_err()
        );
        assert_eq!(
            NodeUrl::with_localhost(8080).to_string(),
            "http://127.0.0.1:8080"
        );
        assert_eq!(
            NodeUrl::with_service(10).to_string(),
            "http://operator-node10:8080"
        );
    }

    #[test]
    fn test_product_symbol_roundtrip() {
        let symbol = ProductSymbol::from_str("ETHP").unwrap();
        let (underlying, product) = symbol.split();
        assert_eq!(
            (underlying, product),
            (
                UnderlyingSymbol::from_str("ETH").unwrap(),
                Product::Perpetual
            )
        );
        let symbol_str = symbol.to_string();
        assert_eq!(symbol_str, "ETHP");
        assert_eq!(symbol, ProductSymbol::from_str(&symbol_str).unwrap());

        #[cfg(feature = "fixed_expiry_future")]
        {
            let symbol = ProductSymbol::from_str("ETHFH").unwrap();
            let (underlying, product) = symbol.split();
            assert_eq!(
                (underlying, product),
                (
                    UnderlyingSymbol::from_str("ETH").unwrap(),
                    Product::QuarterlyExpiryFuture { month_code: 'H' },
                )
            );
            let symbol_str = symbol.to_string();
            assert_eq!(symbol_str, "ETHFH");
            assert_eq!(symbol, ProductSymbol::from_str(&symbol_str).unwrap());
        }
    }
}
