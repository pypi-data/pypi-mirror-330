use crate::{constants::EXEC_OUTCOME_MSG_MAX_SIZE, types::transaction::ExecutionOps};
use anyhow::{Error, anyhow};
use serde::{Deserialize, Serialize};
use std::{convert::TryFrom, string::String};

#[derive(thiserror::Error, Debug)]
pub enum ExecutionError {
    #[error("Skippable error {} - Roll-back the state", _0)]
    Skippable(String),
}

/// The result of a transaction execution including possible recoverable errors
///
/// Execution is a multi step process, this delivers a `PostProcessingRequest` containing
/// the inputs for commitment in untrusted context.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ExecutionOutcome {
    Success(ExecutionOps),
    Skip(String),
}

impl From<ExecutionError> for ExecutionOutcome {
    fn from(e: ExecutionError) -> Self {
        match e {
            ExecutionError::Skippable(e) => {
                let mut msg = format!("{:?}", e);
                msg.truncate(EXEC_OUTCOME_MSG_MAX_SIZE);
                ExecutionOutcome::Skip(msg)
            }
        }
    }
}

impl TryFrom<ExecutionOutcome> for ExecutionError {
    type Error = Error;

    fn try_from(value: ExecutionOutcome) -> Result<Self, Self::Error> {
        match value {
            ExecutionOutcome::Skip(inner) => Ok(ExecutionError::Skippable(inner)),
            ExecutionOutcome::Success(_) => Err(anyhow!(
                "Trying to convert ExecutionOutcome::Success into ExecutionError"
            )),
        }
    }
}

pub type ExecutionResult<T> = Result<T, ExecutionError>;

#[macro_export]
macro_rules! skip_if {
    ($guard: expr, $msg: expr) => {
        if $guard {
            return Err(ExecutionError::Skippable($msg));
        }
    };
    ($guard: expr) => {
        $guard.map_err(|e| ExecutionError::Skippable(e.to_string()))
    };
}

#[cfg(test)]
pub mod tests {
    use core::convert::TryInto;

    use crate::{ExecutionError, ExecutionOutcome, types::transaction::ExecutionOps};

    #[test]
    fn try_from_execution_error_to_outcome() {
        let msg = "A".to_string();
        match ExecutionOutcome::Skip(msg.clone()).try_into().unwrap() {
            ExecutionError::Skippable(s) if s == msg => {}
            _ => panic!("Invalid conversion"),
        }
    }

    #[test]
    #[should_panic]
    fn try_from_execution_error_to_outcome_panics() {
        let _x: ExecutionError = ExecutionOutcome::Success(ExecutionOps::default())
            .try_into()
            .unwrap();
    }
}
