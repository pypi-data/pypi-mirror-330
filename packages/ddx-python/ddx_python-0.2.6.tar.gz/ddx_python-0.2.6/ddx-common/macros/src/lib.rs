use proc_macro::TokenStream;
use proc_macro2::{Ident, Span};
use quote::quote;
use rust_decimal::Decimal;
use syn::{
    Arm, Expr, ExprField, GenericArgument, Item, ItemFn, PathArguments, PathSegment, Stmt, Type,
    parse_macro_input, parse_quote,
};

/// Runs a setup routine to initialize global app context.
#[proc_macro_attribute]
pub fn setup(_metadata: TokenStream, input: TokenStream) -> TokenStream {
    let mut input_fn = parse_macro_input!(input as ItemFn);
    let tracing_init_call = quote! {
        {
            let _ = ddx_common::util::tracing::init_tracing(ddx_common::util::tracing::StdoutFormat::Pretty);
        }
    };
    let parsed_code = syn::parse2(tracing_init_call).expect("Parsing error in the setup macro");

    input_fn.block.stmts.insert(0, parsed_code);

    TokenStream::from(quote! {
        #input_fn
    })
}

const ARRAY: &str = "Vec";
const HASHMAP: &str = "HashMap";
const BTREEMAP: &str = "BTreeMap";
const LINMAP: &str = "LinearMap";
const BYTE: &str = "u8";
const UINT64: &str = "U64";
const STRING: &str = "String";

fn parse_dec(input: TokenStream) -> Decimal {
    let mut source = input.to_string();

    // If it starts with `- ` then get rid of the extra space
    // to_string will put a space between tokens
    if source.starts_with("- ") {
        source.remove(1);
    }
    // Using JSON to serialize to avoid using the std
    let json = format!(r#""{}""#, &source[..]);
    match serde_json::from_str(json.as_str()) {
        Ok(d) => d,
        Err(e) => panic!("Unexpected decimal format for {}: {}", source, e),
    }
}

#[proc_macro]
pub fn dec(input: TokenStream) -> TokenStream {
    let unpacked = parse_dec(input).unpack();
    // We need to further unpack these for quote for now
    let lo = unpacked.lo;
    let mid = unpacked.mid;
    let hi = unpacked.hi;
    let negative = unpacked.negative;
    let scale = unpacked.scale;
    let expanded = quote! {
        ::rust_decimal::Decimal::from_parts(#lo, #mid, #hi, #negative, #scale)
    };
    expanded.into()
}

#[proc_macro]
pub fn unscaled(input: TokenStream) -> TokenStream {
    let unpacked = parse_dec(input).unpack();
    let lo = unpacked.lo;
    let mid = unpacked.mid;
    let hi = unpacked.hi;
    let negative = unpacked.negative;
    let scale = unpacked.scale;
    let expanded = quote! {
        ddx_common::types::primitives::UnscaledI128::new(::rust_decimal::Decimal::from_parts(#lo, #mid, #hi, #negative, #scale))
    };
    expanded.into()
}

#[proc_macro_derive(AsKeccak256)]
pub fn keccak256(input: TokenStream) -> TokenStream {
    let item = parse_macro_input!(input as Item);
    let name = match item {
        Item::Struct(s) => s.ident,
        Item::Enum(e) => e.ident,
        _ => panic!("Only struct and enum are supported"),
    };
    let expanded = quote! {
        impl Keccak256<ddx_common::types::primitives::Hash> for #name {
            fn keccak256(&self) -> ddx_common::types::primitives::Hash {
                let token = ddx_common::util::tokenize::Tokenizable::into_token(self.clone());
                let message = ddx_common::ethabi::encode(&[token]);
                let mut keccak = tiny_keccak::Keccak::new_keccak256();
                keccak.update(&message);

                let mut res: [u8; 32] = [0; 32];
                keccak.finalize(&mut res);
                res.into()
            }
        }
    };
    expanded.into()
}

#[proc_macro_derive(EventDefinition)]
pub fn event_definition(input: TokenStream) -> TokenStream {
    let item = parse_macro_input!(input as Item);
    match item {
        Item::Struct(s) => {
            let name = s.ident;
            let expanded = quote! {
                impl EventDefinition for #name {
                    fn signature(&self) -> H256 {
                        self.0.signature()
                    }
                }
            };
            expanded.into()
        }
        _ => panic!("only structs supported"),
    }
}

#[proc_macro_derive(Nonced)]
pub fn nonced(input: TokenStream) -> TokenStream {
    let item = parse_macro_input!(input as Item);
    match item {
        Item::Struct(s) => {
            let name = s.ident;
            let expanded = quote! {
                impl Nonced for #name {
                    fn nonce(&self) -> Nonce {
                        self.nonce
                    }
                }
            };
            expanded.into()
        }
        Item::Enum(e) => {
            let name = e.ident;
            let mut arms: Vec<Arm> = vec![];
            for v in e.variants.into_iter() {
                let vname = v.ident;
                arms.push(parse_quote! {
                    #name::#vname(inner) => inner.nonce(),
                });
            }
            let expanded = quote! {
                impl Nonced for #name {
                        fn nonce(&self) -> Nonce {
                        match self {
                            #(#arms)*
                        }
                    }
                }
            };
            expanded.into()
        }
        _ => panic!("only structs and enums supported"),
    }
}

#[proc_macro_derive(SignedEIP712)]
pub fn signed_eip712(input: TokenStream) -> TokenStream {
    let item = parse_macro_input!(input as Item);
    match item {
        Item::Struct(s) => {
            let name = s.ident;
            let expanded = quote! {
                impl SignedEIP712 for #name {
                    fn signature(&self) -> Signature {
                        self.signature.clone()
                    }
                }
            };
            expanded.into()
        }
        _ => panic!("only structs supported"),
    }
}

#[proc_macro_derive(AbiToken)]
pub fn abi_token(input: TokenStream) -> TokenStream {
    let item = parse_macro_input!(input as Item);
    let expanded = match item {
        Item::Struct(s) => {
            let name = &s.ident;
            let mut from_token_stmts: Vec<Stmt> = vec![];
            let mut into_token_stmts: Vec<Stmt> = vec![];
            // A wrapper is the New Type pattern.
            // We don't wrap wrappers in a tuple like we do struct with multiple fields.
            let mut is_wrapper = s.fields.len() == 1;
            for (i, field) in s.fields.iter().enumerate() {
                let (val, key): (ExprField, Ident) = if let Some(ident) = &field.ident {
                    is_wrapper = false;
                    (parse_quote! { self.#ident }, ident.clone())
                } else {
                    (
                        parse_quote! { self.0 },
                        Ident::new("field", Span::call_site()),
                    )
                };
                // Each field may require multiple statements to make the token
                into_token_stmts.extend(into_token(&Expr::Field(val), &field.ty));
                if is_wrapper {
                    from_token_stmts.extend(from_token(&key, &field.ty));
                } else {
                    if i == 0 {
                        let stmt: Stmt = parse_quote! {
                            let mut token_stream = match token {
                                ddx_common::ethabi::Token::Tuple(v) => v,
                                _ => ddx_common::bail!("Not a tuple"),
                            };
                        };
                        from_token_stmts.push(stmt);
                    }
                    let stmts: Vec<Stmt> = parse_quote! {
                        ddx_common::ensure!(token_stream.len() > 0, "No token left at this position");
                        // Take the next token in order
                        let token = token_stream.remove(0);
                    };
                    from_token_stmts.extend(stmts);
                    from_token_stmts.extend(from_token(&key, &field.ty));
                }
            }
            let struct_stmts: Vec<Stmt> = if is_wrapper {
                parse_quote! {
                    #(#from_token_stmts)*
                    Ok(#name(field))
                }
            } else {
                let keys = s
                    .fields
                    .iter()
                    .cloned()
                    .map(|f| f.ident.unwrap())
                    .collect::<Vec<Ident>>();
                parse_quote! {
                    #(#from_token_stmts)*
                    Ok(#name {
                        #(#keys),*
                    })
                }
            };
            quote! {
                impl ddx_common::util::tokenize::Tokenizable for #name {
                    fn from_token(token: ddx_common::ethabi::Token) -> ddx_common::Result<Self> {
                        #(#struct_stmts)*
                    }

                    fn into_token(self) -> ddx_common::ethabi::Token {
                        let mut token_stream: Vec<ddx_common::ethabi::Token> = std::vec![];
                        #(#into_token_stmts)*
                        if #is_wrapper {
                            token_stream.pop().expect("One token")
                        } else {
                            ddx_common::ethabi::Token::Tuple(token_stream)
                        }
                    }
                }
            }
        }
        Item::Enum(e) => {
            let name = &e.ident;
            let mut into_token_arms: Vec<Arm> = vec![];
            // From tokens is inverse match statement as into. It takes
            // the discriminant (first token of the tuple) and (if needed) instantiate
            // using the field values decoded from the remaining tokens.
            let mut from_token_arms: Vec<Arm> = vec![];
            for (i, variant) in e.variants.iter().enumerate() {
                let var_name = &variant.ident;
                // Set the discriminant of this variant to its position in the list
                let discriminant = i as u64;
                // The discriminant value of each variant is its 0..N position index
                if variant.fields.is_empty() {
                    // If the selected enum is the variant name, we return the the discriminant
                    into_token_arms.push(
                        parse_quote! { #name::#var_name => std::vec![ddx_common::ethereum_types::U256::from(#discriminant).into_token()], },
                    );
                    // If we decode this discriminant, return this variant
                    from_token_arms.push(parse_quote! {
                        #discriminant => #name::#var_name,
                    });
                } else {
                    let mut into_arm_stmts: Vec<Stmt> = vec![];
                    let mut from_arm_stmts: Vec<Stmt> = vec![];
                    let mut keys = vec![];
                    let mut is_struct = false;
                    for (pos, field) in variant.fields.iter().enumerate() {
                        let ty = &field.ty;
                        let key = if let Some(ident) = &field.ident {
                            // Structured enums are handled like structs
                            let key = ident.clone();
                            let val = parse_quote! { #key };
                            // Execute in the scope of the key variable, encode the field value into token
                            into_arm_stmts.extend(into_token(&Expr::Path(val), ty));
                            is_struct = true;
                            key
                        } else {
                            // We treat all fields as unamed and assign one based on their position
                            // We dereference into these variable names which allows us to call
                            // into_token on these variable names.
                            let name = format!("field_{:?}", pos);
                            let key = Ident::new(name.as_str(), Span::call_site());
                            let val = parse_quote! { #key };
                            into_arm_stmts.extend(into_token(&Expr::Path(val), ty));
                            key
                        };
                        let stmts: Vec<Stmt> = parse_quote! {
                            ddx_common::ensure!(token_stream.len() > 0, "No token left at this position");
                            // Take out the first struct token
                            let token = token_stream.remove(0);
                        };
                        from_arm_stmts.extend(stmts);
                        // Now that we've isolated the token, generate the from_token instructions
                        from_arm_stmts.extend(from_token(&key, ty));
                        // Variables in scope of the arm function
                        keys.push(key);
                    }
                    // TODO: Remove duplicate code by isolating destructuring of keys
                    if is_struct {
                        into_token_arms.push(parse_quote! {
                            #name::#var_name{#(#keys),*} => {
                                let mut token_stream: Vec<ddx_common::ethabi::Token> = std::vec![];
                                token_stream.push(ddx_common::ethereum_types::U256::from(#discriminant).into_token());
                                // // Fields (if any) follow the discriminant
                                #(#into_arm_stmts)*
                                token_stream
                            }
                        });
                        from_token_arms.push(parse_quote! {
                            #discriminant => {
                                #(#from_arm_stmts)*
                                #name::#var_name{#(#keys),*}
                            }
                        });
                    } else {
                        into_token_arms.push(parse_quote! {
                            #name::#var_name(#(#keys),*) => {
                                let mut token_stream: Vec<ddx_common::ethabi::Token> = std::vec![];
                                token_stream.push(ddx_common::ethereum_types::U256::from(#discriminant).into_token());
                                // Fields (if any) follow the discriminant
                                #(#into_arm_stmts)*
                                token_stream
                            }
                        });
                        from_token_arms.push(parse_quote! {
                            #discriminant => {
                                #(#from_arm_stmts)*
                                #name::#var_name(#(#keys),*)
                            }
                        });
                    }
                }
            }
            from_token_arms.push(parse_quote! {
                _ => ddx_common::bail!("Discriminant out of bounds"),
            });
            quote! {
                impl ddx_common::util::tokenize::Tokenizable for #name {
                    fn from_token(token: ddx_common::ethabi::Token) -> ddx_common::Result<Self> {
                        // An enum is always wrapped in a tuple
                        let mut token_stream = match token {
                            ddx_common::ethabi::Token::Tuple(v) => v,
                            _ => ddx_common::bail!("Not a tuple"),
                        };
                        ddx_common::ensure!(token_stream.len() > 0, "Empty token stream");
                        // The sequential number identifying the enum variant
                        // Removing the first item (discriminant) leaves only the fields in the token stream
                        let discriminant = ddx_common::ethereum_types::U256::from_token(token_stream.remove(0))?.as_u64();
                        let var = match discriminant {
                            #(#from_token_arms)*
                        };
                        Ok(var)
                    }

                    fn into_token(self) -> ddx_common::ethabi::Token {
                        // Returns the tokenized discriminant + fields
                        let token_stream: Vec<ddx_common::ethabi::Token> = match self {
                            #(#into_token_arms)*
                        };
                        ddx_common::ethabi::Token::Tuple(token_stream)
                    }
                }
            }
        }
        _ => panic!("Only struct and enum are supported"),
    };
    expanded.into()
}

fn into_token(val: &Expr, ty: &Type) -> Vec<Stmt> {
    if let Type::Path(path) = ty {
        let top_segment = path
            .path
            .segments
            .first()
            .expect("there must be at least 1 segment");
        let ident = &top_segment.ident;
        // The next sections deal with collection wrappers. An alternative to any special processing
        // here would be to implement `Vec<T: Tokenizable>` and `HashMap<T: Tokenizable, T: Tokenizable>`
        // just like we do single types. This would have the advantage of allowing such collections
        // to be nested together. I find this approach intuitive but haven't given much thought
        // to the alternative.
        if ident == ARRAY {
            let item_type = find_bracketed_type(top_segment, BracketedItemPos::First);
            if item_type == BYTE {
                // We have a token type for byte arrays, no need to create another one
                parse_quote! {
                    token_stream.push(#val.into_token());
                }
            } else {
                // Make a token with each item then wrap into an array token
                parse_quote! {
                    let mut tokens: Vec<ddx_common::ethabi::Token> = std::vec![];
                    for item in #val {
                       tokens.push(item.into_token());
                    }
                    token_stream.push(ddx_common::ethabi::Token::Array(tokens));
                }
            }
        } else if ident == HASHMAP || ident == BTREEMAP || ident == LINMAP {
            let key_type = find_bracketed_type(top_segment, BracketedItemPos::First);
            let value_type = find_bracketed_type(top_segment, BracketedItemPos::Second);
            let map_sort_quote = if ident == HASHMAP {
                quote! {
                    // If item is a hashmap, sort by keys to make encoding deterministic
                    pairs.sort_unstable_by_key(|(k, _)| k.clone());
                }
            } else {
                quote! {}
            };
            parse_quote! {
                let mut pairs: Vec<(#key_type, #value_type)> =
                    #val.iter().map(|(k, v)| (k.clone(), v.clone())).collect();
                #map_sort_quote
                let mut key_tokens: Vec<ddx_common::ethabi::Token> = std::vec![];
                let mut value_tokens: Vec<ddx_common::ethabi::Token> = std::vec![];
                for (key, value) in pairs.into_iter() {
                    key_tokens.push(key.into_token());
                    value_tokens.push(value.into_token());
                }
                // A mapping is a tuple of two arrays
                let tokens = std::vec![
                    ddx_common::ethabi::Token::Array(key_tokens),
                    ddx_common::ethabi::Token::Array(value_tokens),
                ];
                token_stream.push(ddx_common::ethabi::Token::Tuple(tokens));
            }
        } else if ident == UINT64 {
            // Ethabi does not support U64 so we pad it into a U256
            parse_quote! {
                token_stream.push(ddx_common::ethereum_types::U256::from(#val.as_u64()).into_token());
            }
        } else if ident == STRING {
            // TODO: The way we wrap Symbol, StrategyId, etc is backwards. Check for overflow on instantiation
            // to avoid the possibility of error here.
            parse_quote! {
                let val_bytes32: ddx_common::types::primitives::Bytes32 = #val.parse().unwrap();
                // TODO: Any way to use the ddx_common path without cyclic dependencies?
                token_stream.push(val_bytes32.into_token());
            }
        } else {
            // Reusing the `Tokenizable` trait for rust-web3. We're using the trait elsewhere
            // when calling smart contracts. The alternative would be to map all types to a param
            // like this: https://github.com/rust-ethereum/ethabi/blob/master/derive/src/lib.rs#L187
            // Our method helps with nested structs because it simply requires that a type
            // implement `into_token()`.
            parse_quote! {
                token_stream.push(#val.into_token());
            }
        }
    } else if let Type::Array(arr) = ty {
        let size = arr.len.clone();
        parse_quote! {
            let mut key_tokens: Vec<ddx_common::ethabi::Token> = Vec::with_capacity(#size);
            let mut value_tokens: Vec<ddx_common::ethabi::Token> = Vec::with_capacity(#size);
            for item in #val {
                // check if address is the empty marker
                if !item.addr.is_empty(){
                    key_tokens.push(item.addr.into_token());
                    value_tokens.push(item.amount.into_token());
                }
            }
            let tokens = std::vec![
                    ddx_common::ethabi::Token::Array(key_tokens),
                    ddx_common::ethabi::Token::Array(value_tokens),
                ];
            token_stream.push(ddx_common::ethabi::Token::Tuple(tokens));
        }
    } else {
        panic!("rlp_derive not supported into token");
    }
}

fn from_token(name: &Ident, ty: &Type) -> Vec<Stmt> {
    if let Type::Path(path) = ty {
        let top_segment = path
            .path
            .segments
            .first()
            .expect("there must be at least 1 segment");
        let ident = &top_segment.ident;
        if ident == ARRAY {
            let item_type = find_bracketed_type(top_segment, BracketedItemPos::First);
            if item_type == BYTE {
                parse_quote! {
                    let #name = token.clone().into_bytes().ok_or_else(|| ddx_common::error!("Bytes array"))?;
                }
            } else {
                parse_quote! {
                    let tokens = token.clone().into_array().ok_or_else(|| ddx_common::error!("Token array"))?;
                    let mut #name = std::vec![];
                    for token in tokens {
                        #name.push(#item_type::from_token(token)?);
                    }
                }
            }
        } else if ident == HASHMAP || ident == BTREEMAP || ident == LINMAP {
            let key_type = find_bracketed_type(top_segment, BracketedItemPos::First);
            let value_type = find_bracketed_type(top_segment, BracketedItemPos::Second);
            let output_map_quote = if ident == HASHMAP {
                quote! {let mut #name = HashMap::new();}
            } else if ident == BTREEMAP {
                quote! {let mut #name = BTreeMap::new();}
            } else if ident == LINMAP {
                quote! {let mut #name = LinearMap::new();}
            } else {
                quote! {}
            };
            if ident == LINMAP {
                parse_quote! {
                    let mut tokens = match token {
                        ddx_common::ethabi::Token::Tuple(v) => v,
                        _ => ddx_common::bail!("Not a tuple"),
                    };
                    ddx_common::ensure!(tokens.len() == 2, "Map in tuple of two");
                    let values = tokens.pop().unwrap().into_array().ok_or_else(|| ddx_common::error!("Token array"))?;
                    let keys = tokens.pop().unwrap().into_array().ok_or_else(|| ddx_common::error!("Token array"))?;
                    #output_map_quote
                    for (key, value) in keys.into_iter().zip(values.into_iter()) {
                        #name.insert(#key_type::from_token(key.clone())?, #value_type::from_token(value)?).unwrap();
                    }
                }
            } else {
                parse_quote! {
                    let mut tokens = match token {
                        ddx_common::ethabi::Token::Tuple(v) => v,
                        _ => ddx_common::bail!("Not a tuple"),
                    };
                    ddx_common::ensure!(tokens.len() == 2, "Map in tuple of two");
                    let values = tokens.pop().unwrap().into_array().ok_or_else(|| ddx_common::error!("Token array"))?;
                    let keys = tokens.pop().unwrap().into_array().ok_or_else(|| ddx_common::error!("Token array"))?;
                    #output_map_quote
                    for (key, value) in keys.into_iter().zip(values.into_iter()) {
                        #name.insert(#key_type::from_token(key.clone())?, #value_type::from_token(value)?);
                    }
                }
            }
        } else if ident == UINT64 {
            // Ethabi does not support U64 so we pad it into a U256
            parse_quote! {
                let #name = ddx_common::ethereum_types::U64::from(ddx_common::ethereum_types::U256::from_token(token.clone())?.as_u64());
            }
        } else if ident == STRING {
            // TODO: The way we wrap Symbol, StrategyId, etc is backwards. Check for overflow on instantiation
            // to avoid the possibility of error here.
            parse_quote! {
                let bytes = token.clone().into_fixed_bytes().ok_or_else(|| ddx_common::error!("Bytes32"))?;
                let str_bytes32 = ddx_common::types::primitives::Bytes32::try_from_slice(&bytes)?;
                let #name = str_bytes32.to_string();
            }
        } else {
            // Reusing the `Tokenizable` trait for rust-web3. We're using the trait elsewhere
            // when calling smart contracts. The alternative would be to map all types to a param
            // like this: https://github.com/rust-ethereum/ethabi/blob/master/derive/src/lib.rs#L187
            // Our method helps with nested structs because it simply requires that a type
            // implement `into_token()`.
            parse_quote! {
                let #name = #ty::from_token(token.clone())?;
            }
        }
    } else if let Type::Array(arr) = ty {
        let item_type = arr.elem.clone();
        let len = arr.len.clone();
        parse_quote! {
            let mut tokens = match token {
                ddx_common::ethabi::Token::Tuple(v) => v,
                _ => ddx_common::bail!("Not a tuple"),
            };
            ddx_common::ensure!(tokens.len() == 2, "Should be in tuple of two");
            let values = tokens.pop().unwrap().into_array().ok_or_else(|| ddx_common::error!("Token array"))?;
            let keys = tokens.pop().unwrap().into_array().ok_or_else(|| ddx_common::error!("Token array"))?;
            let mut #name = [#item_type::default(); #len];
            for (i,(key, value)) in keys.into_iter().zip(values.into_iter()).enumerate() {
                let token = ddx_common::ethabi::Token::Tuple(vec![key, value]);
                #name[i] = #item_type::from_token(token)?;
            }
        }
    } else {
        panic!("rlp_derive not supported from token");
    }
}

enum BracketedItemPos {
    First,
    Second,
}

fn find_bracketed_type(segment: &PathSegment, pos: BracketedItemPos) -> &Ident {
    if let PathArguments::AngleBracketed(angle) = &segment.arguments {
        let arg = match pos {
            BracketedItemPos::First => angle.args.first().expect("Type arg"),
            BracketedItemPos::Second => &angle.args[1],
        };
        if let GenericArgument::Type(Type::Path(path)) = arg {
            &path.path.segments.first().expect("First arg").ident
        } else {
            panic!("Mapping has a key type");
        }
    } else {
        unreachable!("Mapping has only one angle bracketed type")
    }
}
