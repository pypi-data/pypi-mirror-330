use crate::types::request::RequestWithReceipt;
use ddx_common::types::state::CmdKind;
use std::collections::HashMap;

// The type definition of outcome from ticking the trusted clock
pub type ClockTickOutcome = (bool, i64, HashMap<CmdKind, RequestWithReceipt>);
