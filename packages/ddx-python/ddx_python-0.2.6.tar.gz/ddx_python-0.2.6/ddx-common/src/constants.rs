use std::mem::size_of;

use ddx_common_macros::dec;
use ethereum_types::{Address, H520};
use libsecp256k1::{curve::Scalar, util::SECRET_KEY_SIZE};

use crate::types::{
    accounting::StrategyId,
    identifiers::SignerAddress,
    primitives::{CompressedKey, CustodianAddress, TraderAddress},
    request::Nonce,
};

// Client requests
pub const REQ_ORDER: i16 = 0;
pub const REQ_MODIFY_ORDER: i16 = 7;
pub const REQ_CANCEL_ORDER: i16 = 1;
pub const REQ_CANCEL_ALL: i16 = 3;
pub const REQ_WITHDRAW: i16 = 4;
pub const REQ_WITHDRAW_DDX: i16 = 5;
pub const REQ_INSURANCE_FUND_WITHDRAW: i16 = 6;
pub const REQ_UPDATE_PROFILE: i16 = 2;
// Init commands
pub const REQ_BLOCK: i16 = 50;
pub const REQ_ADVANCE_SETTLEMENT_EPOCH: i16 = 51;
pub const REQ_MINT_PRICE_CHECKPOINT: i16 = 53;
pub const REQ_UPDATE_PRODUCT_LISTINGS: i16 = 55;
pub const REQ_ADVANCE_TIME: i16 = 54;
pub const REQ_ADVANCE_EPOCH: i16 = 60;
pub const NB_INIT_CMDS: usize = 5;
// Other commands
pub const REQ_PRICE: i16 = 71;
// Disaster recovery
pub const REQ_DISASTER_RECOVERY: i16 = 80;
// Special genesis request
pub const REQ_GENESIS: i16 = 99;
pub const REQ_BUFFER_SIZE: u64 = 1024 * 128;

// TODO: Clean this up to standardize or merge the req and tx kinds.
// Tx log types
pub const TX_PARTIAL_FILL: i16 = 0;
pub const TX_COMPLETE_FILL: i16 = 1;
pub const TX_POST: i16 = 2;
pub const TX_CANCEL: i16 = 3;
pub const TX_CANCEL_ALL: i16 = 30;
pub const TX_LIQUIDATION: i16 = 4;
pub const TX_STRATEGY_UPDATE: i16 = 5;
pub const TX_TRADER_UPDATE: i16 = 6;
pub const TX_WITHDRAW: i16 = 7;
pub const TX_WITHDRAW_DDX: i16 = 8;
pub const TX_PRICE_CHECKPOINT: i16 = 9;
pub const TX_PNL_REALIZATION: i16 = 10;
pub const TX_FUNDING: i16 = 11;
#[cfg(feature = "fixed_expiry_future")]
pub const TX_FUTURES_EXPIRY: i16 = 17;
pub const TX_TRADE_MINING: i16 = 12;
pub const TX_SPECS_UPDATE: i16 = 13;
pub const TX_TRADABLE_PRODUCT_UPDATE: i16 = 18;
pub const TX_INSURANCE_FUND_UPDATE: i16 = 14;
pub const TX_INSURANCE_FUND_WITHDRAW: i16 = 15;
pub const TX_DISASTER_RECOVERY: i16 = 16;
pub const TX_SIGNER_REGISTERED: i16 = 60;
pub const TX_EPOCH_MARKER: i16 = 100;
pub const TX_FEE_DISTRIBUTION: i16 = 70;
pub const TX_NO_TRANSITION: i16 = 999;

// Special request types for the Raft consensus
pub const RAFT_CLUSTER_NAME: &str = "ddx-epoch-0";
pub const RAFT_BLANK: i16 = 100;
pub const RAFT_CONFIG_CHANGE: i16 = 101;
pub const RAFT_SNAPSHOT_POINTER: i16 = 102;
pub const RAFT_NORMAL: i16 = 103;

// Default 3mib max
pub const RAFT_MAX_SNAPSHOT_CHUNK_SIZE: u64 = 3 * 1024 * 1024;
pub const RAFT_SNAPSHOT_EPOCHS: u64 = 12;
pub const RAFT_HEARTBEAT_INTERVAL_IN_MS: u64 = 50;
pub const RAFT_ENTRY_BUFFER_SIZE: u64 = 65_536;
pub const RAFT_INSTALL_SNAPSHOT_BUFFER_SIZE: usize = 1024;
// TODO 2684: Using a low value to troubleshoot observed timeouts
pub const RAFT_MAX_PAYLOAD_ENTRIES: u64 = 1;
// TODO: Watch out for this, make sure to handle each timeout correctly.
pub const RAFT_DEFAULT_WAIT_TIMEOUT_IN_SECS: u64 = 10 * 60;
pub const RAFT_SNAPSHOT_POLLING_INTERVAL_IN_SECS: u64 = 5;
// Very large 5 minutes election timeout used if not user specified.
pub const RAFT_MIN_ELECTION_TIMEOUT_IN_MS: u64 = 1000 * 60 * 5;
// Large snapshot timeout because snapshots can be large
pub const RAFT_SNAPSHOT_TIMEOUT_IN_MS: u64 = 1000 * 60 * 60;

pub static ENCLAVE_DIR: &str = ".ddx";

// Message passing during enclave context switches
pub const SEAL_LOG_SIZE: usize = 2048;
pub const SEAL_DATA_BUFFER_SIZE: usize = 8192;
pub const LEAF_VALUE_BUFFER_SIZE: usize = 1024;
pub const LEAF_CHUNK_SIZE: usize = 1000;
// TODO: Static buffer size not yet verified.
pub const TICK_BUFFER_SIZE: usize = 4096;
pub const EXEC_OUTCOME_MSG_MAX_SIZE: usize = 1024;
pub const EXEC_OUTCOME_BUFFER_SIZE: usize = 16 * 1024;

pub const FIRST_EPOCH_ID: u64 = 1;
pub const GENESIS_EPOCH_ID: u64 = 0;
pub const GENESIS_TIME_VALUE: u64 = 0;
pub const GENESIS_REQUEST_INDEX: u64 = 1;
// Postgres sequential numbers start at 1 by default
pub const FIRST_PROCESSED_REQUEST_INDEX: u64 = 6;
pub const FIRST_ASSIGNED_REQUEST_INDEX: u64 = 6;

pub const DEFAULT_PG_POOL_SIZE: usize = 8;
pub const SEQUENCER_MAX_POOL_SIZE: usize = 16;

// Symmetric crypto
pub const MIN_CIPHERTEXT_SIZE: usize = 4 + 1;
pub const MAX_PLAINTEXT_SIZE: usize = 8192;
pub const ENCRYPTED_CONTEXT_SUFFIX_SIZE: usize = 12 + 33;

// FIXME: A lot of the constants used here are not appropriate for production.
pub const DEFAULT_TEST_CLOCK_TICK_MS: u64 = 10; // Using 10 ms for tests only.
pub const DEFAULT_CLOCK_TICK_MS: u64 = 1000;
pub const DEFAULT_EPOCH_LEN: u64 = 20; // 200 ms epoch for development only

pub const DEFAULT_PRICE_CHECKPOINT_INTERVAL: u64 = 2; // Price checkpoint should match the block time for development only
// TODO: Ideally, we'd be able to use a lower value for this multiplier;
// however, the trade mining parameters are currently hardcoded into the
// contracts. With this in mind, it takes 48 epochs to be able to be able
// to withdraw DDX from trade mining.
//
pub const DEFAULT_SETTLEMENT_EPOCH_MULTIPLIER: u64 = 48;
pub const DEFAULT_PNL_REALIZATION_SETTLEMENT_MULTIPLIER: u64 = 3;
pub const DEFAULT_FUNDING_SETTLEMENT_MULTIPLIER: u64 = 1;
pub const DEFAULT_TRADE_MINING_DURATION_IN_SETTLEMENT_EPOCHS: u64 = 3;
pub const DEFAULT_TRADE_MINING_SETTLEMENT_MULTIPLIER: u64 = 1;
#[cfg(feature = "fixed_expiry_future")]
pub const DEFAULT_EXPIRY_PRICE_LEAVES_DURATION: u64 = 100;
// These are included for convenience, but settlement period lengths
// should always be expressed in terms of epoch multipliers outside of tests.
pub const DEFAULT_SETTLEMENT_EPOCH_LEN: u64 =
    DEFAULT_EPOCH_LEN * DEFAULT_SETTLEMENT_EPOCH_MULTIPLIER;
pub const DEFAULT_PNL_REALIZATION_PERIOD_LEN: u64 =
    DEFAULT_SETTLEMENT_EPOCH_LEN * DEFAULT_PNL_REALIZATION_SETTLEMENT_MULTIPLIER;
pub const DEFAULT_FUNDING_PERIOD_LEN: u64 =
    DEFAULT_SETTLEMENT_EPOCH_LEN * DEFAULT_FUNDING_SETTLEMENT_MULTIPLIER;
pub const DEFAULT_TRADE_MINING_PERIOD_LEN: u64 =
    DEFAULT_SETTLEMENT_EPOCH_LEN * DEFAULT_TRADE_MINING_SETTLEMENT_MULTIPLIER;

// Trade mining reward delay in ticks applied to maker orders.
pub const TRADE_MINING_REWARD_DELAY: u64 = 1;

pub const DEFAULT_NB_CONFIRMATIONS: u64 = 6;
pub const DEFAULT_PORT_RANGE_START: u16 = 11000;
pub const DEFAULT_EMA_PERIODS: u64 = 30;
pub const LOCALHOST_ADDRESS: &str = "127.0.0.1";

pub const GENESIS_SNAPSHOT_ID: &str = "genesis-snapshot";
pub const STATE_SNAPSHOT_PREFIX: &str = "epoch";
pub const NODE_LABEL_PREFIX: &str = "node";
// See "--format" variants in [pg_dump](https://www.postgresql.org/docs/13/app-pgdump.html)
pub const PG_DUMP_FORMAT: &str = "custom";
pub const PG_DUMP_COMPRESSION: u64 = 2;
pub const PG_DUMP_DIR: &str = "/var/local/dexlabs/dumps";
pub const BUFFER_DUMP_DIR: &str = "/var/local/dexlabs/buffers";
pub const STATE_SNAPSHOT_FILENAME: &str = "snapshot.bin";
// Timeout when waiting for an expected pg_dump file.
// Keep relatively high as a job can be long running.
pub const PG_DUMP_TIMEOUT_IN_MS: u64 = 1000 * 60;
// TODO: Make much smaller after more testing as this is on the execution path
pub const PG_DUMP_STARTUP_TIMEOUT_IN_MS: u64 = 1000 * 60;
pub const PG_DUMP_MIN_EXPECTED_SIZE: usize = 1024;
pub const PG_SQL_FILE: &str = "migrations.sql";
pub const PG_STATE_SCHEMA_NAME: &str = "state";
pub const PG_VSTATE_SCHEMA_NAME: &str = "verified_state";
pub const PG_REQUEST_SCHEMA_NAME: &str = "request";
pub const PG_KYC_SCHEMA_NAME: &str = "trusted_kyc";
pub const PG_COPY_TRADING_SQL_NAME: &str = "copy-trading.sql";
pub const PG_COPY_TRADING_SCHEMA_NAME: &str = "trusted_copy_trading";
pub const PG_OPERATOR_SCHEMA_NAME: &str = "operator";
pub const PG_RESTORE_PREFIX: &str = "restore";
pub const PG_DATABASE_NAME: &str = "derivadex";

pub const FILE_EXIST_POLLING_INTERVAL_IN_MS: u64 = 800;

pub const CHAIN_ETHEREUM: u8 = 0;
pub const CHAIN_ID_ETHEREUM_MAINNET: u64 = 1;

// The capacity of the contract event cache.
// Set high enough to the sequencer being ahead of the processor.
pub const BLOCK_CACHE_CAPACITY: u64 = 50;

// The maximum anticipated number of collaterals supported.
// If this number is too high for the current buffer values, some quickcheck tests would fail.
pub const MAX_COLLATERAL_TYPES: usize = 2;

#[cfg(any(test, feature = "test_harness"))]
pub const DUMMY_PRNG_SEED: [u8; 32] = [
    1, 0, 0, 0, 23, 0, 0, 0, 200, 1, 0, 0, 210, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0,
];

// Shared buffer size
pub const KYC_MAX_LEN: usize = 1024;
pub const ENCRYPTED_CONTENT_MAX_LEN: usize = 1024;
// Cryptography related.
pub const AES_KEY_LEN: usize = 16;
pub const AES_NONCE_LEN: usize = 12;
pub const AES_TAG_LEN: usize = 16;
pub const SCALAR_BYTE_LEN: usize = size_of::<Scalar>();
pub const SECRET_KEY_LEN: usize = SECRET_KEY_SIZE;
pub const SIGNATURE_BYTE_LEN: usize = size_of::<H520>();
pub const ADDRESS_BYTE_LEN: usize = size_of::<Address>();
pub const COMPRESSED_KEY_BYTE_LEN: usize = CompressedKey::BYTE_LEN;
pub const SIGNER_ADDRESS_BYTE_LEN: usize = size_of::<SignerAddress>();
pub const CUSTODIAN_ADDRESS_BYTE_LEN: usize = CustodianAddress::BYTE_LEN;
pub const TRADER_ADDRESS_BYTE_LEN: usize = TraderAddress::BYTE_LEN;
pub const NONCE_BYTE_LEN: usize = size_of::<Nonce>();
// This value is manually evaluated since `AttestationUserData` is a private type in `ddx-common-enclave`.
pub const USER_DATA_LEN: usize = ADDRESS_BYTE_LEN * 2;
pub const KECCAK256_DIGEST_SIZE: usize = 256 / 8;
pub const STRATEGY_ID_BYTE_LEN: usize = size_of::<StrategyId>();

pub const MIN_COLLATERAL: rust_decimal::Decimal = dec!(0.000001);

// Unit for scaling up decimals to integer representing units of tokens (i.e. 10**18)
pub const TOKEN_UNIT_SCALE: u32 = 6;
// The max decimal number than can be scaled to u128 and then unscaled back to Decimal without overflowing
// Calculated with: Decimal::MAX / Decimal::exp10(6)
pub const MAX_UNSCALED_DECIMAL: rust_decimal::Decimal = dec!(79228162514264337593543.950335);

// Default gas values large enough to avoid most out-of-gas error in development
pub const LARGE_GAS_LIMIT: u64 = 5_999_999;
pub const LARGE_GAS_PRICE: u64 = 10_000_000;

pub const IMF_FACTOR: f64 = 0.0004;

// Reasonable upper bound for requests to replay at startup
// TODO 2416: Reduce to keep catch up time under 10-20 minutes.
pub const REQUEST_LOG_BUFFER: usize = 5000;
pub const HOLDING_STASH_CAP: usize = 1_000;

pub const DEFAULT_CURRENCY_DECIMAL_PRECISION: u32 = 4;

pub const RUNTIME_MAX_WORKER_THREADS: usize = 4;
pub const RUNTIME_MIN_BLOCKING_THREADS: usize = 1;
// Must be less than `Enclave.config.xml`
pub const TCS_NUM: usize = 12;
// Trusted tokio runtime number of threads
pub const TRUSTED_RUNTIME_NUM_THREADS: usize = 4;

pub const REQUEST_LOG_MAX_GAP: u64 = 50;

pub const TX_LOG_RELAY_BUFFER: usize = 1_000;
pub const MAX_RAFT_COMMIT_DURATION_IN_MS: u128 = 30_000;

pub const TX_LOG_HEAD_CHUNK_SIZE: usize = 100;
pub const STATE_LEAVES_CHUNK_SIZE: usize = 100;
pub const WS_MSG_PAUSE_IN_MS: u64 = 2;
// TODO: Please update the parameters without the alpha guard.
#[cfg(not(any(feature = "alpha1", feature = "no_rate_limit")))]
pub const RATE_LIMIT_TIER1_MIN_DDX_BALANCE: u64 = 1_000;
#[cfg(feature = "alpha1")]
pub const RATE_LIMIT_TIER1_MIN_DDX_BALANCE: u64 = 1_000;
#[cfg(not(feature = "no_rate_limit"))]
pub const RATE_LIMIT_TIER2_MIN_DDX_BALANCE: u64 = RATE_LIMIT_TIER1_MIN_DDX_BALANCE * 1000;

#[cfg(not(feature = "no_rate_limit"))]
pub const RATE_LIMIT_TIER1: u64 = 1;
#[cfg(not(feature = "no_rate_limit"))]
pub const RATE_LIMIT_TIER2: u64 = 2;

/// How often we refresh (pull data from verified state) the trader cache
pub const TRADER_CACHE_EXPIRY_IN_MS: u64 = 15 * 1000;
/// Grace period for claiming a sequencing outcome
///
/// Requests are only idempotent during this time period.
pub const TRADER_CACHE_OUTCOME_EXPIRY_IN_SECS: u64 = 60 * 2;
/// How long we keep the trader cache around after last access
///
/// Outcomes are also removed after this lifetime expires.
pub const TRADER_CACHE_LIFETIME_IN_SECS: u64 = 5 * 60;
/// How often do we check the cache lifetime for expiry
pub const TRADER_CACHE_SHRINK_INTERVAL_IN_SECS: u64 = 60;

pub const DEFAULT_REPLAY_PAGE_SIZE: u64 = 1000;

// Rate limit parameters.
// TODO 2043: Make sure this is tuned sensibly
// TODO 2043: In addition to this, make nginx throttle rate 0 ips that reach their bucket limit
// TODO: Please update the parameters without the alpha guard.
#[cfg(not(any(feature = "alpha1", feature = "no_rate_limit")))]
pub const RATE_LIMIT_PER_HOUR_TIER0: u32 = 3600;
#[cfg(feature = "alpha1")]
pub const RATE_LIMIT_PER_HOUR_TIER0: u32 = 3600; // 3600 is one req/sec on average
#[cfg(not(feature = "no_rate_limit"))]
pub const RATE_LIMIT_BURST_TIER0: u32 = 1; // Hard cap - bursting up to N cells at once
#[cfg(not(feature = "no_rate_limit"))]
pub const RATE_LIMIT_PER_HOUR_TIER1: u32 = 3600 * 5;
#[cfg(not(feature = "no_rate_limit"))]
pub const RATE_LIMIT_BURST_TIER1: u32 = 5;
#[cfg(not(feature = "no_rate_limit"))]
pub const RATE_LIMIT_PER_HOUR_TIER2: u32 = 3600 * 50;
// On the webserver layer, the burst limit is the number of inbound requests that can accumulate in
// the inbound sequencer channel. Reaching this limit will simply delay responses. Errors would follow
// only if the excess requests somehow made it through to the trusted sequencer. In addition, the first
// layer of defense should be nginx enforcing the same burst limit.
#[cfg(not(feature = "no_rate_limit"))]
pub const RATE_LIMIT_BURST_CAP: u32 = 50;
#[cfg(feature = "no_rate_limit")]
pub const RATE_LIMIT_BURST_CAP: u32 = 100000;

pub const INSURANCE_FUND_MINIMUM_SIZE_POST_WITHDRAW_USDC: u32 = 1_000_000;

/// This dummy ddx perp symbol is used to avoid unnecessary complexity in the codebase.
///
/// DDX_SYMBOL cannot be used for tradable products.
/// This dummy symbol is solely used for price feed and DDX fee discount purposes.
pub const fn dummy_ddx_perp() -> &'static str {
    "DDXP"
}

pub const USDC_SYMBOL: &str = "USDC";
pub const DDX_FEE_DISCOUNT: rust_decimal::Decimal = dec!(0.5);

pub const PRICE_FEED_POLLING_INTERVAL_IN_MS: u64 = 1000;
// The maximum allowed delay between price feed updates
pub const PRICE_FEED_DELAY_THRESHOLD_SECONDS: u64 = 600;

pub const DB_COMMITTER_CHANNEL_SIZE: usize = 100;

pub const MEMBERSHIP_REQUEST_LIFESPAN_SECONDS: i64 = 300;

/// A number of ticks (= seconds) that is the maximum age of a DDX price checkpoint
pub const MAX_DDX_PRICE_CHECKPOINT_AGE_IN_TICKS: usize = 40_000;

/// The maximum allowed delay between kyc auth updates
pub const KYC_AUTH_EXPIRY_BLOCK_DELTA: u64 = 7199;

// NTS protocol for secured timestamp
pub const DEFAULT_NTP_PORT: u16 = 123;
pub const DEFAULT_KE_PORT: u16 = 4460;
pub const NTS_HOSTNAME_0: &str = "time.cloudflare.com";
pub const NTS_HOSTNAME_1: &str = "virginia.time.system76.com";
pub const NTS_HOSTNAME_2: &str = "nts.netnod.se";
pub const NTS_TIME_TOLERANCE_MS: u64 = 200;

// Coingecko Hostname and DDX contract address
pub const COINGECKO_HOSTNAME: &str = "api.coingecko.com";
pub const DDX_CONTRACT_ADDRESS: &str = "0x3a880652f47bfaa771908c07dd8673a787daed3a";
pub const COINGECKO_POLL_THRESHOLD: usize = 60;

// Default limit on strategies a trader can have
pub const MAX_STRATEGIES: u8 = 10;

// Default submit withdrawal threshold for the eth bridge
pub const SUBMIT_WITHDRAWAL_THRESHOLD: u64 = 1000000;

// Snapshot eth rpc url
pub const SNAPSHOT_ETH_RPC_URL: &str = "http://ethereum:8545";
// Alchemy endpoint path
pub const ALCHEMY_ENDPOINT_PATH: &str = "g.alchemy.com/v2/";

// DDX application id for smart contract storage, padded to fit 32 bytes
pub const DDX_APPLICATION_ID: &[u8; 32] = b"exchange-operator\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0";
pub const DDX_APPLICATION_ID_LEN: usize = 17;
