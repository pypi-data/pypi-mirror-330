use crate::ethereum_types::Address;
use ddx_common_macros::AbiToken;
use ethereum_types::U128;

#[derive(Debug, Clone, PartialEq, AbiToken)]
pub struct Signer {
    /// The custodian address of the signer.
    pub custodian: Address,
}

#[derive(Debug, Clone, PartialEq, AbiToken)]
pub struct CustodianWithoutSigners {
    /// The DDX balance of the custodian.
    pub balance: U128,
    /// The block in which the custodian can unbond themselves.
    pub unbond_eta: U128,
    /// Indicates whether or not the custodian is approved to register
    /// signers.
    pub approved: bool,
    /// Indicates whether or not the custodian was jailed due to submitting
    /// a non-matching hash or at the discretion of governance.
    pub jailed: bool,
}
