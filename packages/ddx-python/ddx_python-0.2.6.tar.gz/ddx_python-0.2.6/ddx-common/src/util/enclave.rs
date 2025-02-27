use crate::types::{
    identifiers::ReleaseHash,
    primitives::{Bytes32, FixedBytesWrapper},
};
use rustc_hex::ToHex;
use serde::{Deserialize, Serialize};
use std::fmt;

#[derive(Clone, Default, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct ReleaseMeasurement {
    pub mr_enclave: Bytes32,
    pub isvsvn: [u8; 2],
    pub release_hash: ReleaseHash,
    pub debug: bool,
}

impl ReleaseMeasurement {
    pub fn new(mr_enclave_slice: &[u8], isvsvn: u16, sgx_debug: bool) -> Self {
        ReleaseMeasurement {
            mr_enclave: Bytes32::from_slice(mr_enclave_slice),
            isvsvn: isvsvn.to_be_bytes(),
            release_hash: ReleaseHash::new(mr_enclave_slice, isvsvn),
            debug: sgx_debug,
        }
    }
}

impl fmt::Debug for ReleaseMeasurement {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("ReleaseMeasurement")
            .field(
                "mr_enclave",
                &format!("0x{}", self.mr_enclave.as_bytes().to_hex::<String>()),
            )
            .field("isvsvn", &format!("0x{}", self.isvsvn.to_hex::<String>()))
            .field(
                "release_hash",
                &format!("0x{}", self.release_hash.0.as_bytes().to_hex::<String>()),
            )
            .finish()
    }
}
