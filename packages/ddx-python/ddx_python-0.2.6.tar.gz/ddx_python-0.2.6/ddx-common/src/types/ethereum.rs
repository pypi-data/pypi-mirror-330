// TODO: A large amount of the types in this file have been taken
// from OpenEthereum. If possible, it would be better to utilize
// these types via a no_std library.
#![allow(non_camel_case_types)]
use crate::{
    constants::KECCAK256_DIGEST_SIZE,
    crypto::Keccak256,
    ethereum_types::{Address, H64, H256, U256},
    types::primitives::Hash as DDXHash,
};
use hash_db::Hasher;
use plain_hasher::PlainHasher;
use rlp::{Encodable, RlpStream};
use serde::{Deserialize, Serialize};
use serde_big_array::big_array;
use serde_repr::*;
use std::{collections::HashMap, mem, ops, vec::Vec};
use tiny_keccak::Keccak;

big_array! { BigArray; }

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Faucet {
    pub address: Address,
    pub private_key: H256,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct ContractAddresses {
    #[serde(rename = "derivaDEXAddress")]
    pub derivadex: Address,
    #[serde(rename = "ddxAddress")]
    pub ddx_token: Address,
    #[serde(rename = "usdcAddress")]
    pub usdc_token: Address,

    #[serde(flatten)]
    pub other: HashMap<String, serde_json::Value>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct DeploymentMeta {
    pub addresses: ContractAddresses,
    pub chain_id: u64,
    pub eth_rpc_url: String,
    pub faucet: Option<Faucet>,
}

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
struct AddressesMeta(HashMap<String, DeploymentMeta>);

impl DeploymentMeta {
    pub fn from_deployment(contract_deployment: &str) -> Self {
        let share_dir = std::env::var("APP_CONFIG").expect("APP_CONFIG not set");
        let mut addresses_path = std::path::PathBuf::from(&share_dir);
        addresses_path.push("ethereum/addresses.json");
        tracing::debug!(
            ?contract_deployment,
            ?addresses_path,
            "Environment app context"
        );
        let f = std::fs::File::open(addresses_path)
            .expect("Cannot initialize app context without addresses.json");
        let data =
            serde_json::from_str::<AddressesMeta>(std::io::read_to_string(f).unwrap().as_str())
                .expect("Cannot parse addresses.json");
        let meta = data
            .0
            .get(contract_deployment)
            .expect("CONTRACT_DEPLOYMENT not found in addresses.json");
        tracing::debug!(
            "Read from addresses.json: {:?} {:?}",
            meta.chain_id,
            meta.addresses
        );
        meta.clone()
    }

    pub fn from_env() -> Self {
        let contract_deployment =
            std::env::var("CONTRACT_DEPLOYMENT").unwrap_or_else(|_| "snapshot".to_string());
        Self::from_deployment(&contract_deployment)
    }
}

#[derive(Debug, Clone, Default, PartialEq, Deserialize, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ConfirmedBlock {
    pub header: BlockHeader,
    pub receipts: Vec<TypedReceipt>,
}

#[derive(Clone, Default, Debug, PartialEq)]
pub struct BlockData {
    pub header: BlockHeader,
    pub receipts: Vec<TypedReceipt>,
}

#[derive(Debug, Default, Clone, PartialEq, Deserialize, Serialize)]
pub struct BlockHeader {
    pub parent_hash: H256,
    pub uncles_hash: H256,
    pub author: Address,
    pub state_root: H256,
    pub transactions_root: H256,
    pub receipts_root: H256,
    pub bloom: Bloom,
    pub difficulty: U256,
    pub number: u64,
    pub gas_limit: U256,
    pub gas_used: U256,
    pub timestamp: u64,
    pub extra_data: Vec<u8>,
    pub mix_hash: Option<H256>,
    pub nonce: Option<H64>,
    // TODO: We should only use this field in the `develop` feature.
    // This doesn't seem to play nicely between packages though.
    pub seal: Vec<Vec<u8>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub base_fee_per_gas: Option<U256>,
    pub withdrawals_root: Option<H256>,
    pub blob_gas_used: Option<U256>,
    pub excess_blob_gas: Option<U256>,
    pub parent_beacon_block_root: Option<H256>,
}

impl Encodable for BlockHeader {
    fn rlp_append(&self, s: &mut RlpStream) {
        let mut extra_fields = self.seal.len();
        if self.base_fee_per_gas.is_some() {
            extra_fields += 1;
        }
        if self.mix_hash.is_some() {
            extra_fields += 1;
        }
        if self.nonce.is_some() {
            extra_fields += 1;
        }
        if self.withdrawals_root.is_some() {
            extra_fields += 1;
        }
        if self.blob_gas_used.is_some() {
            extra_fields += 1;
        }
        if self.excess_blob_gas.is_some() {
            extra_fields += 1;
        }
        if self.parent_beacon_block_root.is_some() {
            extra_fields += 1;
        }
        s.begin_list(13 + extra_fields);
        s.append(&self.parent_hash.as_ref());
        s.append(&self.uncles_hash.as_ref());
        s.append(&self.author.as_ref());
        s.append(&self.state_root.as_ref());
        s.append(&self.transactions_root.as_ref());
        s.append(&self.receipts_root.as_ref());
        s.append(&self.bloom.contents.as_ref());
        append_u256(s, &self.difficulty);
        s.append(&self.number);
        append_u256(s, &self.gas_limit);
        append_u256(s, &self.gas_used);
        s.append(&self.timestamp);
        s.append(&self.extra_data);
        if let Some(mix_hash) = self.mix_hash {
            s.append(&mix_hash.as_ref());
        }
        if let Some(nonce) = self.nonce {
            s.append(&nonce.as_ref());
        }
        for b in &self.seal {
            s.append_raw(b, 1);
        }
        if let Some(base_fee_per_gas) = self.base_fee_per_gas {
            append_u256(s, &base_fee_per_gas);
        }
        if let Some(withdrawals_root) = self.withdrawals_root {
            s.append(&withdrawals_root.as_ref());
        }
        if let Some(blob_gas_used) = self.blob_gas_used {
            append_u256(s, &blob_gas_used);
        }
        if let Some(excess_blob_gas) = self.excess_blob_gas {
            append_u256(s, &excess_blob_gas);
        }
        if let Some(parent_beacon_block_root) = self.parent_beacon_block_root {
            s.append(&parent_beacon_block_root.as_ref());
        }
    }
}

fn append_u256(s: &mut RlpStream, v: &U256) {
    let leading_empty_bytes = 32 - (v.bits() + 7) / 8;
    let mut buffer = [0u8; 32];
    v.to_big_endian(&mut buffer);
    s.append(&buffer[leading_empty_bytes..].as_ref());
}

impl BlockHeader {
    pub fn hash(&self) -> DDXHash {
        rlp::encode(self).keccak256().into()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Deserialize, Serialize)]
pub enum TransactionOutcome {
    Unknown,
    StateRoot(H256),
    StatusCode(u8),
}

#[derive(Clone, PartialEq, Eq, Deserialize, Serialize)]
pub struct LegacyReceipt {
    pub gas_used: U256,
    pub bloom: Bloom,
    pub logs: Vec<LogEntry>,
    pub outcome: TransactionOutcome,
}

impl std::fmt::Debug for LegacyReceipt {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        f.debug_struct("LegacyReceipt")
            .field("gas_used", &self.gas_used)
            .field("bloom", &self.bloom)
            .field("logs_summary", &self.logs.iter().map(LogSummary::from))
            .field("outcome", &self.outcome)
            .finish()
    }
}

impl LegacyReceipt {
    pub fn new(outcome: TransactionOutcome, gas_used: U256, logs: Vec<LogEntry>) -> Self {
        LegacyReceipt {
            gas_used,
            bloom: logs.iter().fold(Bloom::default(), |mut b, l| {
                b.accrue_bloom(&l.bloom());
                b
            }),
            logs,
            outcome,
        }
    }

    pub fn rlp_append(&self, s: &mut RlpStream) {
        match self.outcome {
            TransactionOutcome::Unknown => {
                s.begin_list(3);
            }
            TransactionOutcome::StateRoot(ref root) => {
                s.begin_list(4);
                s.append(&root.as_ref());
            }
            TransactionOutcome::StatusCode(ref status_code) => {
                s.begin_list(4);
                s.append(status_code);
            }
        }
        append_u256(s, &self.gas_used);
        s.append(&self.bloom.contents.as_ref());
        s.append_list(&self.logs);
    }
}

#[derive(Serialize_repr, Eq, Hash, Deserialize_repr, Debug, Copy, Clone, PartialEq)]
#[repr(u8)]
pub(crate) enum TypedTxId {
    EIP4484Transaction = 0x03,
    EIP1559Transaction = 0x02,
    AccessList = 0x01,
    Legacy = 0x00,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum TypedReceipt {
    Legacy(LegacyReceipt),
    AccessList(LegacyReceipt),
    EIP1559Transaction(LegacyReceipt),
    EIP4484Transaction(LegacyReceipt),
}

impl TypedReceipt {
    #[cfg(test)]
    pub(crate) fn new(type_id: TypedTxId, legacy_receipt: LegacyReceipt) -> Self {
        //currently we are using same receipt for both legacy and typed transaction
        match type_id {
            TypedTxId::EIP4484Transaction => Self::EIP4484Transaction(legacy_receipt),
            TypedTxId::EIP1559Transaction => Self::EIP1559Transaction(legacy_receipt),
            TypedTxId::AccessList => Self::AccessList(legacy_receipt),
            TypedTxId::Legacy => Self::Legacy(legacy_receipt),
        }
    }

    pub(super) fn encode(&self) -> Vec<u8> {
        match self {
            Self::Legacy(receipt) => {
                let mut s = RlpStream::new();
                receipt.rlp_append(&mut s);
                s.as_raw().to_vec()
            }
            Self::AccessList(receipt) => {
                let mut rlps = RlpStream::new();
                receipt.rlp_append(&mut rlps);
                [&[TypedTxId::AccessList as u8], rlps.as_raw()].concat()
            }
            Self::EIP1559Transaction(receipt) => {
                let mut rlps = RlpStream::new();
                receipt.rlp_append(&mut rlps);
                [&[TypedTxId::EIP1559Transaction as u8], rlps.as_raw()].concat()
            }
            Self::EIP4484Transaction(receipt) => {
                let mut rlps = RlpStream::new();
                receipt.rlp_append(&mut rlps);
                [&[TypedTxId::EIP4484Transaction as u8], rlps.as_raw()].concat()
            }
        }
    }
}

#[allow(dead_code)]
#[derive(Default, Debug, Clone)]
struct LogSummary {
    address: Address,
    topics: Vec<H256>,
    size: usize,
    tx_hash: H256,
}

impl From<&LogEntry> for LogSummary {
    fn from(log: &LogEntry) -> Self {
        LogSummary {
            address: log.address,
            topics: log.topics.clone(),
            size: log.data.len(),
            tx_hash: log.tx_hash,
        }
    }
}

#[derive(Default, Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LogEntry {
    pub address: Address,
    pub topics: Vec<H256>,
    pub data: Vec<u8>,
    // TODO: This isn't trusted and thus shouldn't be used for anything security
    // critical. This seems fine for now since it's primarily used in the frontend.
    pub tx_hash: H256,
}

impl LogEntry {
    pub(super) fn bloom(&self) -> Bloom {
        self.topics.iter().fold(
            Bloom::from(Input::Raw(self.address.as_bytes())),
            |mut b, t| {
                b.accrue(Input::Raw(t.as_bytes()));
                b
            },
        )
    }
}

impl Encodable for LogEntry {
    fn rlp_append(&self, s: &mut RlpStream) {
        s.begin_list(3).append(&self.address.as_ref());
        s.begin_list(self.topics.len());
        for topic in &self.topics {
            s.append(&topic.as_ref());
        }
        s.append(&self.data);
    }
}

// 3 according to yellowpaper
const BLOOM_BITS: u32 = 3;
const BLOOM_SIZE: usize = 256;

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
pub struct Bloom {
    #[serde(with = "BigArray")]
    pub contents: [u8; BLOOM_SIZE],
}

impl Default for Bloom {
    fn default() -> Self {
        Self {
            contents: [0; BLOOM_SIZE],
        }
    }
}

fn log2(x: usize) -> u32 {
    if x <= 1 {
        return 0;
    }

    let n = x.leading_zeros();
    mem::size_of::<usize>() as u32 * 8 - n
}

pub enum Input<'a> {
    Raw(&'a [u8]),
    Hash(&'a [u8; KECCAK256_DIGEST_SIZE]),
}

enum Hash<'a> {
    Ref(&'a [u8; KECCAK256_DIGEST_SIZE]),
    Owned([u8; KECCAK256_DIGEST_SIZE]),
}

impl<'a> From<Input<'a>> for Hash<'a> {
    fn from(input: Input<'a>) -> Self {
        match input {
            Input::Raw(raw) => Hash::Owned(raw.keccak256()),
            Input::Hash(hash) => Hash::Ref(hash),
        }
    }
}

impl ops::Index<usize> for Hash<'_> {
    type Output = u8;

    fn index(&self, index: usize) -> &u8 {
        match *self {
            Hash::Ref(r) => &r[index],
            Hash::Owned(ref hash) => &hash[index],
        }
    }
}

impl Hash<'_> {
    fn len(&self) -> usize {
        match *self {
            Hash::Ref(r) => r.len(),
            Hash::Owned(ref hash) => hash.len(),
        }
    }
}

impl<'a> PartialEq<BloomRef<'a>> for Bloom {
    fn eq(&self, other: &BloomRef<'a>) -> bool {
        let s_ref: &[u8] = &self.contents;
        let o_ref: &[u8] = other.0;
        s_ref.eq(o_ref)
    }
}

impl<'a> From<Input<'a>> for Bloom {
    fn from(input: Input<'a>) -> Bloom {
        let mut bloom = Bloom::default();
        bloom.accrue(input);
        bloom
    }
}

impl Bloom {
    fn accrue(&mut self, input: Input<'_>) {
        let p = BLOOM_BITS;

        let m = self.contents.len();
        let bloom_bits = m * 8;
        let mask = bloom_bits - 1;
        let bloom_bytes = (log2(bloom_bits) + 7) / 8;

        let hash: Hash<'_> = input.into();

        // must be a power of 2
        assert_eq!(m & (m - 1), 0);
        // out of range
        assert!(p * bloom_bytes <= hash.len() as u32);

        let mut ptr = 0;

        assert_eq!(BLOOM_BITS, 3);
        for i in 0..3 {
            let _ = i;
            let mut index = 0_usize;
            for _ in 0..bloom_bytes {
                index = (index << 8) | hash[ptr] as usize;
                ptr += 1;
            }
            index &= mask;
            self.contents[m - 1 - index / 8] |= 1 << (index % 8);
        }
    }

    pub(super) fn accrue_bloom<'a, B>(&mut self, bloom: B)
    where
        BloomRef<'a>: From<B>,
    {
        let bloom_ref: BloomRef<'_> = bloom.into();
        assert_eq!(self.contents.len(), BLOOM_SIZE);
        assert_eq!(bloom_ref.0.len(), BLOOM_SIZE);
        for i in 0..BLOOM_SIZE {
            self.contents[i] |= bloom_ref.0[i];
        }
    }
}

#[derive(Clone, Copy)]
pub struct BloomRef<'a>(&'a [u8; BLOOM_SIZE]);

impl<'a> From<&'a Bloom> for BloomRef<'a> {
    fn from(bloom: &'a Bloom) -> Self {
        BloomRef(&bloom.contents)
    }
}

#[cfg(not(target_family = "wasm"))]
#[tracing::instrument(level = "debug", skip_all, fields(receipts=%receipts.len()))]
pub fn extract_contract_events_from_receipts(
    receipts: Vec<TypedReceipt>,
) -> crate::Result<Vec<super::contract_events::ContractEvent>> {
    let logs = receipts
        .into_iter()
        .map(|r| {
            let receipt = match r {
                TypedReceipt::Legacy(receipt) => receipt,
                TypedReceipt::AccessList(receipt) => receipt,
                TypedReceipt::EIP1559Transaction(receipt) => receipt,
                TypedReceipt::EIP4484Transaction(receipt) => receipt,
            };
            receipt.logs
        })
        .fold(vec![], |mut acc, v| {
            acc.extend(v);
            acc
        });
    let contract_address = crate::global::app_context().contract_address;
    tracing::debug!(
        ?contract_address,
        "Parsing events from {:?} logs",
        logs.len(),
    );
    let events = logs
        .into_iter()
        .filter(|l| {
            tracing::trace!(?l.address, ?contract_address, is_empty=?l.topics.is_empty(), event_sigs=?crate::types::contract_events::all_event_signatures(), "Filtering contract event");
            l.address == contract_address
                && !l.topics.is_empty()
                && crate::types::contract_events::all_event_signatures().contains(&l.topics[0])
        })
        .map(crate::types::contract_events::decode_contract_events)
        .fold(vec![], |mut acc, v| {
            acc.extend(v);
            acc
        });
    Ok(events)
}

/// Concrete `Hasher` impl for the Keccak-256 hash
#[derive(Default, Debug, Clone, PartialEq)]
struct KeccakHasher;
impl Hasher for KeccakHasher {
    type Out = H256;
    type StdHasher = PlainHasher;
    const LENGTH: usize = KECCAK256_DIGEST_SIZE;
    fn hash(x: &[u8]) -> Self::Out {
        let mut out = [0; KECCAK256_DIGEST_SIZE];
        Keccak::keccak256(x, &mut out);
        out.into()
    }
}

fn ordered_trie_root<I, V>(input: I) -> H256
where
    I: IntoIterator<Item = V>,
    V: AsRef<[u8]>,
{
    triehash::ordered_trie_root::<KeccakHasher, I>(input)
}

pub fn calculate_receipts_root(receipts: &[TypedReceipt]) -> H256 {
    ordered_trie_root(receipts.iter().map(|r| r.encode()))
}

#[cfg(test)]
mod test {
    use super::*;
    use crate::crypto::from_hex;
    use anyhow::Result;
    use std::str::FromStr;

    #[test]
    fn test_block_hash1() -> Result<()> {
        let expected_hash: DDXHash =
            H256::from_str("0x2b5101ecfbaaddd4e37fb21ab43096888ff0e7d25e2e89eb7b3c807965232e73")?
                .into();
        let mut bloom = [0; BLOOM_SIZE];
        bloom.copy_from_slice(&from_hex("0x10204000400000011002000080220001101210000000000000000040a800c0000000810000c004000800708008810100023080040a000800000000030830280500000006006221030882000800002070008010001400021000800404c0056120520000000200000080050000000088000010842022004040080008b4010d00200000a02800040000820000002000200000001021110800080020804608104010128c8004000038024a0200b10808801090000001200000041000000808000080000020030000002020000000000c110008000200000a801600801180c00220002138200800000000000400000100000080000004010080404000180000005000")?[..256]);
        let header = BlockHeader {
            parent_hash: H256::from_str(
                "0x9889ed9e78d883433f6599ede659dfc5105ba69b3ad33fefc8e83e92efdf8409",
            )?,
            uncles_hash: H256::from_str(
                "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
            )?,
            author: Address::from_str("0x52bc44d5378309ee2abf1539bf71de1b7d7be3b5")?,
            state_root: H256::from_str(
                "0x64591c628e1fec6f8309c4ac05c2b0568974da809337fba2ca14929aa0f805a9",
            )?,
            transactions_root: H256::from_str(
                "0xe1ff2b3f490298cbd69bd6c8f94af9aa6d95774c53ca16e2729ee4c1b447f022",
            )?,
            receipts_root: H256::from_str(
                "0xd7fd3b9e7a22b2dcaeb3ef2aaf237bac3ee4679f6e5bfe82bb6eb0e9858a5451",
            )?,
            bloom: Bloom { contents: bloom },
            difficulty: U256::from(8926624369618029_u64),
            number: 13284899,
            gas_limit: U256::from(30000000),
            gas_used: U256::from(2169791),
            timestamp: 1632438972,
            extra_data: vec![110, 97, 110, 111, 112, 111, 111, 108, 46, 111, 114, 103],
            mix_hash: Some(H256::from_str(
                "0x2fba3c00a2a942df87df4941562e288fce6678a90b2a9479352683d4a0df20d6",
            )?),
            nonce: Some(H64::from_str("0x5305755edef1be39")?),
            seal: Default::default(),
            base_fee_per_gas: Some(U256::from(59032141527_u64)),
            withdrawals_root: None,
            blob_gas_used: None,
            excess_blob_gas: None,
            parent_beacon_block_root: None,
        };
        assert_eq!(header.hash(), expected_hash);

        Ok(())
    }

    #[test]
    fn test_block_hash2() -> Result<()> {
        let expected_hash: DDXHash =
            H256::from_str("0x4fed6603f749a4bd18a5e3cd21922327a18b20167d084e9e25a36e0a3ffcb334")?
                .into();
        let mut bloom = [0; BLOOM_SIZE];
        let bloom_bytes = from_hex(
            "0xe1f500c004995004205e0bc3a4008fa98e1123f47cd2081410710010d0b721144222d104302663930051004041dc219442c338c007077381853076a400bf73020a3564120444292cca0e816b227c92e441004008074cf821e0dcac02e22001b1c24461205ea027236008b8e400b6e9d511c3007260096e48e0290790c4280844338a21e56a17e86a244b1440e0312810408804c96847818c0429314850da31c00605102f912290281a0030c3164c302a24546252258600089101174c272242724d3044a2a10cd8582d80109185e6de0381e9080000e861dc091371821f466b2236d0642da2538c20800299a200560a12a2110a2c5990074481e21883220a4708",
        )?;
        bloom.copy_from_slice(&bloom_bytes[..BLOOM_SIZE]);
        let header = BlockHeader {
            parent_hash: H256::from_str(
                "0x1469313981cb69286cbfbda5c4e9e02018ca6b091939e99cb888ff3fc5ae8cb7",
            )?,
            uncles_hash: H256::from_str(
                "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
            )?,
            author: Address::from_str("0x4d496ccc28058b1d74b7a19541663e21154f9c84")?,
            state_root: H256::from_str(
                "0x347343a7b838d95ce12f36f12bdc2bdd9e52ca7f7b83fc82bd3ed3fb72973fdd",
            )?,
            transactions_root: H256::from_str(
                "0x0163a0f504da105424bac01fa7919072af1c3ddc25a041b867f10f5415e7e0b7",
            )?,
            receipts_root: H256::from_str(
                "0x357f0a0a8c1d51fb7bc487e0b2022ebbbad9f3af47fc48ae5c095766c5e4cf72",
            )?,
            bloom: Bloom { contents: bloom },
            difficulty: Default::default(),
            number: 8656123,
            gas_limit: 30000000_u64.into(),
            gas_used: 29992912_u64.into(),
            timestamp: 1678832784,
            extra_data: from_hex("0xd883010b04846765746888676f312e32302e32856c696e7578")?,
            mix_hash: Some(H256::from_str(
                "0xf570e9f413634790998f5af69d0abcd77db8c83f6f8a94496c1ff9b160e4f2c8",
            )?),
            nonce: Some(Default::default()),
            seal: Default::default(),
            base_fee_per_gas: Some(3048311736_u64.into()),
            withdrawals_root: Some(H256::from_str(
                "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
            )?),
            blob_gas_used: None,
            excess_blob_gas: None,
            parent_beacon_block_root: None,
        };
        assert_eq!(header.hash(), expected_hash);

        Ok(())
    }

    #[test]
    fn test_no_state_root() {
        let expected: Vec<u8> = rustc_hex::FromHex::from_hex("f9014183040caeb9010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000f838f794dcf421d093428b096ca501a7cd1a740855a7976fc0a00000000000000000000000000000000000000000000000000000000000000000").unwrap();
        let r = TypedReceipt::new(
            TypedTxId::Legacy,
            LegacyReceipt::new(
                TransactionOutcome::Unknown,
                0x40cae.into(),
                vec![LogEntry {
                    address: Address::from_str("dcf421d093428b096ca501a7cd1a740855a7976f").unwrap(),
                    topics: vec![],
                    data: vec![0u8; 32],
                    tx_hash: H256::zero(),
                }],
            ),
        );
        assert_eq!(r.encode(), expected);
    }

    #[test]
    fn test_basic_legacy() {
        let expected: Vec<u8> = rustc_hex::FromHex::from_hex("f90162a02f697d671e9ae4ee24a43c4b0d7e15f1cb4ba6de1561120d43b9a4e8c4a8a6ee83040caeb9010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000f838f794dcf421d093428b096ca501a7cd1a740855a7976fc0a00000000000000000000000000000000000000000000000000000000000000000").unwrap();
        let r = TypedReceipt::new(
            TypedTxId::Legacy,
            LegacyReceipt::new(
                TransactionOutcome::StateRoot(
                    H256::from_str(
                        "2f697d671e9ae4ee24a43c4b0d7e15f1cb4ba6de1561120d43b9a4e8c4a8a6ee",
                    )
                    .unwrap(),
                ),
                0x40cae.into(),
                vec![LogEntry {
                    address: Address::from_str("dcf421d093428b096ca501a7cd1a740855a7976f").unwrap(),
                    topics: vec![],
                    data: vec![0u8; 32],
                    tx_hash: H256::zero(),
                }],
            ),
        );
        let encoded = r.encode();
        assert_eq!(encoded, expected);
    }

    #[test]
    fn test_basic_access_list() {
        let expected: Vec<u8> = rustc_hex::FromHex::from_hex("01f90162a02f697d671e9ae4ee24a43c4b0d7e15f1cb4ba6de1561120d43b9a4e8c4a8a6ee83040caeb9010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000f838f794dcf421d093428b096ca501a7cd1a740855a7976fc0a00000000000000000000000000000000000000000000000000000000000000000").unwrap();
        let r = TypedReceipt::new(
            TypedTxId::AccessList,
            LegacyReceipt::new(
                TransactionOutcome::StateRoot(
                    H256::from_str(
                        "2f697d671e9ae4ee24a43c4b0d7e15f1cb4ba6de1561120d43b9a4e8c4a8a6ee",
                    )
                    .unwrap(),
                ),
                0x40cae.into(),
                vec![LogEntry {
                    address: Address::from_str("dcf421d093428b096ca501a7cd1a740855a7976f").unwrap(),
                    topics: vec![],
                    data: vec![0u8; 32],
                    tx_hash: H256::zero(),
                }],
            ),
        );
        let encoded = r.encode();
        assert_eq!(&encoded, &expected);
    }

    #[test]
    fn test_basic_eip1559() {
        let expected: Vec<u8> = rustc_hex::FromHex::from_hex("02f90162a02f697d671e9ae4ee24a43c4b0d7e15f1cb4ba6de1561120d43b9a4e8c4a8a6ee83040caeb9010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000f838f794dcf421d093428b096ca501a7cd1a740855a7976fc0a00000000000000000000000000000000000000000000000000000000000000000").unwrap();
        let r = TypedReceipt::new(
            TypedTxId::EIP1559Transaction,
            LegacyReceipt::new(
                TransactionOutcome::StateRoot(
                    H256::from_str(
                        "2f697d671e9ae4ee24a43c4b0d7e15f1cb4ba6de1561120d43b9a4e8c4a8a6ee",
                    )
                    .unwrap(),
                ),
                0x40cae.into(),
                vec![LogEntry {
                    address: Address::from_str("dcf421d093428b096ca501a7cd1a740855a7976f").unwrap(),
                    topics: vec![],
                    data: vec![0u8; 32],
                    tx_hash: H256::zero(),
                }],
            ),
        );
        let encoded = r.encode();
        assert_eq!(&encoded, &expected);
    }

    #[test]
    fn test_status_code() {
        let expected: Vec<u8> = rustc_hex::FromHex::from_hex("f901428083040caeb9010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000f838f794dcf421d093428b096ca501a7cd1a740855a7976fc0a00000000000000000000000000000000000000000000000000000000000000000").unwrap();
        let r = TypedReceipt::new(
            TypedTxId::Legacy,
            LegacyReceipt::new(
                TransactionOutcome::StatusCode(0),
                0x40cae.into(),
                vec![LogEntry {
                    address: Address::from_str("dcf421d093428b096ca501a7cd1a740855a7976f").unwrap(),
                    topics: vec![],
                    data: vec![0u8; 32],
                    tx_hash: H256::zero(),
                }],
            ),
        );
        let encoded = r.encode();
        assert_eq!(&encoded[..], &expected[..]);
    }
}
