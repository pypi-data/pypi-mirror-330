use std::mem::size_of;

use crate::{
    Result, ensure, error,
    ethabi::{ParamType, Token},
    ethereum_types::{Address, H256, H520, U128, U256},
};
use arrayvec::ArrayVec;
use serde::{Deserialize, Serialize};

// TODO: I took the `Tokenizable` and `Tokenize` trait and implementation in the
// module from Rust Web3. I didn't want to import the whole thing and didn't have
// a way to get just this feature. I'll ask them to create one, but everything we
// need is here in the meantime.

/// Tokens conversion trait
pub trait Tokenize {
    /// Convert to list of tokens
    fn into_tokens(self) -> Vec<Token>;
}

impl Tokenize for &[Token] {
    fn into_tokens(self) -> Vec<Token> {
        self.to_vec()
    }
}

impl<T: Tokenizable> Tokenize for T {
    fn into_tokens(self) -> Vec<Token> {
        vec![self.into_token()]
    }
}

impl Tokenize for () {
    fn into_tokens(self) -> Vec<Token> {
        vec![]
    }
}

macro_rules! impl_tokens {
  ($( $ty: ident : $no: tt, )+) => {
    impl<$($ty, )+> Tokenize for ($($ty,)+) where
      $(
        $ty: Tokenizable,
      )+
    {
      fn into_tokens(self) -> Vec<Token> {
        vec![
          $( self.$no.into_token(), )+
        ]
      }
    }
  }
}

impl_tokens!(A:0, );
impl_tokens!(A:0, B:1, );
impl_tokens!(A:0, B:1, C:2, );
impl_tokens!(A:0, B:1, C:2, D:3, );
impl_tokens!(A:0, B:1, C:2, D:3, E:4, );
impl_tokens!(A:0, B:1, C:2, D:3, E:4, F:5, );
impl_tokens!(A:0, B:1, C:2, D:3, E:4, F:5, G:6, );
impl_tokens!(A:0, B:1, C:2, D:3, E:4, F:5, G:6, H:7, );
impl_tokens!(A:0, B:1, C:2, D:3, E:4, F:5, G:6, H:7, I:8, );
impl_tokens!(A:0, B:1, C:2, D:3, E:4, F:5, G:6, H:7, I:8, J:9, );
impl_tokens!(A:0, B:1, C:2, D:3, E:4, F:5, G:6, H:7, I:8, J:9, K:10, );
impl_tokens!(A:0, B:1, C:2, D:3, E:4, F:5, G:6, H:7, I:8, J:9, K:10, L:11, );
impl_tokens!(A:0, B:1, C:2, D:3, E:4, F:5, G:6, H:7, I:8, J:9, K:10, L:11, M:12, );
impl_tokens!(A:0, B:1, C:2, D:3, E:4, F:5, G:6, H:7, I:8, J:9, K:10, L:11, M:12, N:13, );
impl_tokens!(A:0, B:1, C:2, D:3, E:4, F:5, G:6, H:7, I:8, J:9, K:10, L:11, M:12, N:13, O:14, );
impl_tokens!(A:0, B:1, C:2, D:3, E:4, F:5, G:6, H:7, I:8, J:9, K:10, L:11, M:12, N:13, O:14, P:15, );

/// Simplified output type for single value.
pub trait Tokenizable {
    /// Converts a `Token` into expected type.
    fn from_token(token: Token) -> Result<Self>
    where
        Self: Sized;
    /// Converts a specified type back into token.
    fn into_token(self) -> Token;
}

impl Tokenizable for Token {
    fn from_token(token: Token) -> Result<Self> {
        Ok(token)
    }
    fn into_token(self) -> Token {
        self
    }
}

impl Tokenizable for String {
    fn from_token(token: Token) -> Result<Self> {
        match token {
            Token::String(s) => Ok(s),
            other => Err(error!("Expected `String`, got {:?}", other)),
        }
    }

    fn into_token(self) -> Token {
        Token::String(self)
    }
}

pub fn token_from_vec<T: Tokenizable>(v: Vec<T>) -> Token {
    Token::Array(v.into_iter().map(T::into_token).collect())
}

pub fn vec_from_token<T: Tokenizable>(token: Token) -> Result<Vec<T>> {
    match token {
        Token::Array(tokens) => tokens.into_iter().map(T::from_token).collect(),
        other => Err(error!("Expected Token::Array(...), got {:?}", other)),
    }
}

impl Tokenizable for H256 {
    fn from_token(token: Token) -> Result<Self> {
        match token {
            Token::FixedBytes(s) => {
                if s.len() != 32 {
                    return Err(error!("Expected `H256`, got {:?}", s));
                }
                let mut data = [0; 32];
                for (idx, val) in s.into_iter().enumerate() {
                    data[idx] = val;
                }
                Ok(data.into())
            }
            other => Err(error!("Expected `H256`, got {:?}", other)),
        }
    }

    fn into_token(self) -> Token {
        Token::FixedBytes(self.as_ref().to_vec())
    }
}

impl Tokenizable for Address {
    fn from_token(token: Token) -> Result<Self> {
        match token {
            Token::Address(data) => Ok(data),
            other => Err(error!("Expected `Address`, got {:?}", other)),
        }
    }

    fn into_token(self) -> Token {
        Token::Address(self)
    }
}

macro_rules! eth_uint_tokenizable {
    ($uint: ident, $name: expr) => {
        impl Tokenizable for $uint {
            fn from_token(token: Token) -> Result<Self> {
                match token {
                    Token::Int(data) | Token::Uint(data) => {
                        Ok(std::convert::TryInto::try_into(data).unwrap())
                    }
                    other => Err(error!("Expected `{}`, got {:?}", $name, other)).into(),
                }
            }

            fn into_token(self) -> Token {
                Token::Uint(self.into())
            }
        }
    };
}

eth_uint_tokenizable!(U256, "U256");
eth_uint_tokenizable!(U128, "U128");

macro_rules! int_tokenizable {
    ($int: ident, $token: ident) => {
        impl Tokenizable for $int {
            fn from_token(token: Token) -> Result<Self> {
                match token {
                    Token::Int(data) | Token::Uint(data) => Ok(data.low_u128() as _),
                    other => Err(error!("Expected `{}`, got {:?}", stringify!($int), other)),
                }
            }

            fn into_token(self) -> Token {
                // this should get optimized away by the compiler for unsigned integers
                #[allow(unused_comparisons)]
                let data = if self < 0 {
                    // NOTE: Rust does sign extension when converting from a
                    // signed integer to an unsigned integer, so:
                    // `-1u8 as u128 == u128::MAX`
                    U256::from(self as u128) | U256([0, 0, u64::MAX, u64::MAX])
                } else {
                    self.into()
                };
                Token::$token(data)
            }
        }
    };
}

int_tokenizable!(i8, Int);
int_tokenizable!(i16, Int);
int_tokenizable!(i32, Int);
int_tokenizable!(i64, Int);
int_tokenizable!(i128, Int);
int_tokenizable!(u8, Uint);
int_tokenizable!(u16, Uint);
int_tokenizable!(u32, Uint);
int_tokenizable!(u64, Uint);
int_tokenizable!(u128, Uint);

impl Tokenizable for bool {
    fn from_token(token: Token) -> Result<Self> {
        match token {
            Token::Bool(data) => Ok(data),
            other => Err(error!("Expected `bool`, got {:?}", other)),
        }
    }
    fn into_token(self) -> Token {
        Token::Bool(self)
    }
}

/// Marker trait for `Tokenizable` types that are can tokenized to and from a
/// `Token::Array` and `Token:FixedArray`.
pub trait TokenizableItem: Tokenizable {}

macro_rules! tokenizable_item {
    ($($type: ty,)*) => {
        $(
            impl TokenizableItem for $type {}
        )*
    };
}

tokenizable_item! {
    Token, String, Address, H256, U256, U128, bool, Vec<u8>,
    i8, i16, i32, i64, i128, u16, u32, u64, u128,
}

impl Tokenizable for Vec<u8> {
    fn from_token(token: Token) -> Result<Self> {
        match token {
            Token::Bytes(data) => Ok(data),
            Token::FixedBytes(data) => Ok(data),
            other => Err(error!("Expected `bytes`, got {:?}", other)),
        }
    }
    fn into_token(self) -> Token {
        Token::Bytes(self)
    }
}

const H520_BYTE_LEN: usize = size_of::<H520>();

impl Tokenizable for [u8; H520_BYTE_LEN] {
    fn from_token(token: Token) -> Result<Self> {
        match token {
            Token::FixedBytes(data) => {
                ensure!(data.len() == H520_BYTE_LEN, "65 bytes token");
                let mut fixed_bytes = [0_u8; H520_BYTE_LEN];
                fixed_bytes.copy_from_slice(&data);
                Ok(fixed_bytes)
            }
            other => Err(error!("Expected `bytes`, got {:?}", other)),
        }
    }
    fn into_token(self) -> Token {
        Token::FixedBytes(self.to_vec())
    }
}

impl<T: TokenizableItem> Tokenizable for Vec<T> {
    fn from_token(token: Token) -> Result<Self> {
        match token {
            Token::FixedArray(tokens) | Token::Array(tokens) => {
                tokens.into_iter().map(Tokenizable::from_token).collect()
            }
            other => Err(error!("Expected `Array`, got {:?}", other)),
        }
    }

    fn into_token(self) -> Token {
        Token::Array(self.into_iter().map(Tokenizable::into_token).collect())
    }
}

impl Tokenizable for H520 {
    fn from_token(token: Token) -> Result<Self> {
        match token {
            // TODO: Why not Token::FixedBytes?
            Token::Bytes(data) => {
                ensure!(data.len() == H520_BYTE_LEN, "65 bytes token");
                let mut fixed_bytes = [0_u8; H520_BYTE_LEN];
                fixed_bytes.copy_from_slice(&data);
                Ok(H520::from_slice(&fixed_bytes))
            }
            other => Err(error!("Expected `bytes`, got {:?}", other)),
        }
    }
    fn into_token(self) -> Token {
        Token::Bytes(self.as_bytes().to_vec())
    }
}

impl<T: TokenizableItem> TokenizableItem for Vec<T> {}

macro_rules! impl_fixed_types {
    ($num: expr) => {
        impl Tokenizable for [u8; $num] {
            fn from_token(token: Token) -> Result<Self> {
                match token {
                    Token::FixedBytes(bytes) => {
                        if bytes.len() != $num {
                            return Err(error!(
                                "Expected `FixedBytes({})`, got FixedBytes({})",
                                $num,
                                bytes.len()
                            ));
                        }

                        let mut arr = [0; $num];
                        arr.copy_from_slice(&bytes);
                        Ok(arr)
                    }
                    other => Err(error!("Expected `FixedBytes({})`, got {:?}", $num, other)).into(),
                }
            }

            fn into_token(self) -> Token {
                Token::FixedBytes(self.to_vec())
            }
        }

        impl TokenizableItem for [u8; $num] {}

        impl<T: TokenizableItem + Clone> Tokenizable for [T; $num] {
            fn from_token(token: Token) -> Result<Self> {
                match token {
                    Token::FixedArray(tokens) => {
                        if tokens.len() != $num {
                            return Err(error!(
                                "Expected `FixedArray({})`, got FixedArray({})",
                                $num,
                                tokens.len()
                            ));
                        }

                        let mut arr = ArrayVec::<T, $num>::new();
                        let mut it = tokens.into_iter().map(T::from_token);
                        for _ in 0..$num {
                            arr.push(it.next().expect("Length validated in guard; qed")?);
                        }
                        // Can't use expect here because [T; $num]: Debug is not satisfied.
                        match arr.into_inner() {
                            Ok(arr) => Ok(arr),
                            Err(_) => panic!("All elements inserted so the array is full; qed"),
                        }
                    }
                    other => Err(error!("Expected `FixedArray({})`, got {:?}", $num, other)),
                }
            }

            fn into_token(self) -> Token {
                Token::FixedArray(
                    ArrayVec::from(self)
                        .into_iter()
                        .map(T::into_token)
                        .collect(),
                )
            }
        }

        impl<T: TokenizableItem + Clone> TokenizableItem for [T; $num] {}
    };
}

impl_fixed_types!(1);
impl_fixed_types!(2);
impl_fixed_types!(3);
impl_fixed_types!(4);
impl_fixed_types!(5);
impl_fixed_types!(6);
impl_fixed_types!(7);
impl_fixed_types!(8);
impl_fixed_types!(9);
impl_fixed_types!(10);
impl_fixed_types!(11);
impl_fixed_types!(12);
impl_fixed_types!(13);
impl_fixed_types!(14);
impl_fixed_types!(15);
impl_fixed_types!(16);
impl_fixed_types!(32);
impl_fixed_types!(64);
impl_fixed_types!(128);
impl_fixed_types!(256);
impl_fixed_types!(512);
impl_fixed_types!(1024);

// End of sources copied from rust-web3

/// Equivalent to `ethabi::ParamType` but serializable
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "t", content = "c")]
pub enum TokenSchema {
    /// Address.
    Address,
    /// Bytes.
    Bytes,
    /// Signed integer.
    Int(usize),
    /// Unsigned integer.
    Uint(usize),
    /// Boolean.
    Bool,
    /// String.
    String,
    /// Array of unknown size.
    Array(Box<TokenSchema>),
    /// Vector of bytes with fixed size.
    FixedBytes(usize),
    /// Array with fixed size.
    FixedArray(Box<TokenSchema>, usize),
    /// Tuple containing different types
    Tuple(Vec<Box<TokenSchema>>),
    /// Placeholder type for empty containers with a mandatory type field
    Void,
}

/// Recursively generates a token schema containing the type and all sub-types of a token
/// The schema is required to use `ethabi::decode`.
pub fn generate_schema(token: &Token) -> TokenSchema {
    match *token {
        Token::Address(_) => TokenSchema::Address,
        Token::Bytes(_) => TokenSchema::Bytes,
        Token::String(_) => TokenSchema::String,
        Token::FixedBytes(ref bytes) => TokenSchema::FixedBytes(bytes.len()),
        Token::Int(int) => TokenSchema::Int(int.0.len() * 64), // Length in 64-bit registries
        // To my knowledge, the `Token` enum only allows the U256 type here, so calculating the
        // length seems redundant.
        Token::Uint(uint) => TokenSchema::Uint(uint.0.len() * 64),
        Token::Bool(_) => TokenSchema::Bool,
        Token::Array(ref tokens) => {
            let inner = match tokens.first() {
                Some(token) => generate_schema(token),
                // Using Bytes as a placeholder for the inner type of empty arrays
                None => TokenSchema::Void,
            };
            TokenSchema::Array(Box::new(inner))
        }
        Token::FixedArray(ref tokens) => {
            let inner = match tokens.first() {
                Some(token) => generate_schema(token),
                // Using Bytes as a placeholder for the inner type of empty arrays
                None => TokenSchema::Void,
            };
            TokenSchema::FixedArray(Box::new(inner), tokens.len())
        }
        Token::Tuple(ref tokens) => TokenSchema::Tuple(
            tokens
                .iter()
                .map(|t| Box::new(generate_schema(t)))
                .collect(),
        ),
    }
}

impl From<TokenSchema> for ParamType {
    /// Converts to the type needed to use the `ethabi::decode` function
    fn from(value: TokenSchema) -> Self {
        match value {
            TokenSchema::Address => ParamType::Address,
            TokenSchema::Bytes => ParamType::Bytes,
            TokenSchema::Int(len) => ParamType::Int(len),
            TokenSchema::Uint(len) => ParamType::Uint(len),
            TokenSchema::Bool => ParamType::Bool,
            TokenSchema::String => ParamType::String,
            TokenSchema::Array(inner) => ParamType::Array(Box::new(ParamType::from(*inner))),
            TokenSchema::FixedBytes(len) => ParamType::FixedBytes(len),
            TokenSchema::FixedArray(inner, len) => {
                ParamType::FixedArray(Box::new(ParamType::from(*inner)), len)
            }
            TokenSchema::Tuple(inner) => {
                ParamType::Tuple(inner.into_iter().map(|v| ParamType::from(*v)).collect())
            }
            // By convention, we map Void to Bool. Since Void only exists to satisfy the inner type
            // requirement of empty arrays, it won't ever actually get decoded into any value
            // so the ParamType given does not matter.
            TokenSchema::Void => ParamType::Bool,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{
        constants::TOKEN_UNIT_SCALE,
        ethabi::{decode, encode},
        types::{
            accounting::{Balance, Strategy},
            primitives::{TokenAddress, TokenSymbol},
        },
    };
    use ddx_common_macros::{AbiToken, dec};
    use std::collections::HashMap;

    #[derive(AbiToken, Debug, Default, PartialEq, Clone)]
    struct TestNewType(U128);

    #[derive(AbiToken, Debug, Default, PartialEq, Clone)]
    struct TestWithNamedFields {
        foo: U128,
        bar: U128,
        many: Vec<U128>,
        raw: Vec<u8>,
        mapping: HashMap<H256, U128>,
        bool: bool,
    }

    #[derive(AbiToken, Debug, PartialEq, Clone)]
    enum Foo {
        A,
        B,
    }

    #[derive(AbiToken, Debug, PartialEq, Clone)]
    enum Bar {
        D,
        E(H256),
        F(H256, U256),
    }

    #[derive(AbiToken, Debug, PartialEq, Clone)]
    struct TestWithSimpleEnum {
        foo: Foo,
    }

    #[derive(AbiToken, Debug, PartialEq, Clone)]
    struct TestWithEnums {
        foo: Foo,
        bar: Bar,
        many: Vec<TestNewType>,
    }

    #[derive(Debug, PartialEq, Clone, AbiToken)]
    pub enum TestComplexEnum {
        Number(Vec<U128>),
        NoTransition,
    }

    #[test]
    fn test_abi_encode_complex_enum() {
        let test = TestComplexEnum::NoTransition;
        let token = test.clone().into_token();
        assert_eq!(format!("{:?}", token), "Tuple([Uint(1)])");
        let test2 = TestComplexEnum::from_token(token).unwrap();
        assert_eq!(test, test2);

        let test = TestComplexEnum::Number(vec![]);
        let token = test.clone().into_token();
        assert_eq!(format!("{:?}", token), "Tuple([Uint(0), Array([])])");
        let test2 = TestComplexEnum::from_token(token).unwrap();
        assert_eq!(test, test2);
    }

    #[test]
    fn test_abi_encode_newtype() {
        let test = TestNewType(U128::zero());
        let token = test.clone().into_token();
        assert_eq!(format!("{:?}", token), "Uint(0)");
        let test2 = TestNewType::from_token(token).unwrap();
        assert_eq!(test, test2);
    }

    #[test]
    fn test_abi_encode_fields() {
        let mut mapping = HashMap::new();
        let _num: U256 = U256::one();
        mapping.insert(H256::zero(), U128::one());
        let test = TestWithNamedFields {
            foo: Default::default(),
            bar: Default::default(),
            many: vec![U128::zero(), U128::one()],
            raw: vec![0_u8, 1_u8],
            mapping,
            bool: true,
        };
        let token = test.clone().into_token();
        let schema = generate_schema(&token);
        let bytes = encode(&[token]);
        let schema_ser = serde_json::to_string(&schema).unwrap();
        assert_eq!(
            schema_ser,
            r#"{"t":"Tuple","c":[{"t":"Uint","c":256},{"t":"Uint","c":256},{"t":"Array","c":{"t":"Uint","c":256}},{"t":"Bytes"},{"t":"Tuple","c":[{"t":"Array","c":{"t":"FixedBytes","c":32}},{"t":"Array","c":{"t":"Uint","c":256}}]},{"t":"Bool"}]}"#
        );
        // Unfortunately, ethabi does not expose `decode_param` which has a better syntax
        let token2 = decode(&[schema.into()], &bytes).unwrap().remove(0);
        assert_eq!(
            format!("{:?}", token2),
            "Tuple([Uint(0), Uint(0), Array([Uint(0), Uint(1)]), Bytes([0, 1]), Tuple([Array([FixedBytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]), Array([Uint(1)])]), Bool(true)])"
        );
        let test2 = TestWithNamedFields::from_token(token2).unwrap();
        assert_eq!(test, test2);
    }

    #[test]
    fn test_abi_encode_with_simple_enum() {
        let test = TestWithSimpleEnum { foo: Foo::A };
        let token = test.clone().into_token();
        assert_eq!(format!("{:?}", token), "Tuple([Tuple([Uint(0)])])");
        let test2 = TestWithSimpleEnum::from_token(token).unwrap();
        assert_eq!(test, test2);
    }

    #[test]
    fn test_abi_encode_with_enums() {
        let test = TestWithEnums {
            foo: Foo::A,
            bar: Bar::E(H256::zero()),
            many: vec![TestNewType::default(), TestNewType(U128::one())],
        };
        let token = test.into_token();
        assert_eq!(
            format!("{:?}", token),
            "Tuple([Tuple([Uint(0)]), Tuple([Uint(1), FixedBytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]), Array([Uint(0), Uint(1)])])"
        );
        let test = TestWithEnums {
            foo: Foo::B,
            bar: Bar::F(H256::zero(), U256::one()),
            many: vec![TestNewType::default(), TestNewType(U128::one())],
        };
        let token = test.into_token();
        assert_eq!(
            format!("{:?}", token),
            "Tuple([Tuple([Uint(1)]), Tuple([Uint(2), FixedBytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), Uint(1)]), Array([Uint(0), Uint(1)])])"
        );
    }

    #[test]
    fn test_abi_encode_strategy() {
        let mut scaled_dec = dec!(1);
        scaled_dec.set_scale(TOKEN_UNIT_SCALE).unwrap();
        let strategy = Strategy {
            avail_collateral: Balance::new(scaled_dec.into(), TokenSymbol::USDC),
            locked_collateral: Balance::new(scaled_dec.into(), TokenSymbol::USDC),
            max_leverage: 20,
            frozen: false,
        };
        let token = strategy.clone().into_token();
        let schema = generate_schema(&token);
        let bytes = encode(&[token]);
        let token2 = decode(&[schema.into()], &bytes).unwrap().remove(0);
        assert_eq!(
            format!("{:?}", token2),
            format!(
                "Tuple([Tuple([Array([Address({})]), Array([Uint(1)])]), Tuple([Array([Address({})]), Array([Uint(1)])]), Uint(20), Bool(false)])",
                TokenAddress::from(TokenSymbol::USDC),
                TokenAddress::from(TokenSymbol::USDC)
            )
        );
        let strategy2 = Strategy::from_token(token2).unwrap();
        assert_eq!(strategy, strategy2);
    }
}
