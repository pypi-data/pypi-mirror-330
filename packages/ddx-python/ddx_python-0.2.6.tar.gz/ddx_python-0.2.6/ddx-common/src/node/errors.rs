use serde::Serialize;
use warp::{http::StatusCode, reject};

#[derive(Clone, Debug)]
pub enum ErrorReason {
    /// 403 - The request contained valid data and was understood by the server, but the server is
    ///     refusing action due to user attempting a prohibited action (ie. making a request when
    ///     operator is transitioning to the epoch of a new release.
    Forbidden,
    /// 422 - The payload cannot be decrypted.
    ///
    /// Blanket error for given bytes cannot be decrypted based on convention.
    InvalidEncryption,
    /// 400 - Payload bytes can be decrypted into a massage, but not deserialized as `Request`.
    InvalidRequestPayload,
    /// 412 - Request `Nonce` exists but not monotonically increasing.
    IllegalNonce,
    /// 401 - Request signer recovered from signature does not exist.
    SignerNotFound,
    /// 404 - KYC auth is expired (not found).
    KycNotFound,
    /// 429 - Request signer is authenticated but rejected by the rate limiter.
    RateLimit,
    /// 421 - Not accepting this kind of request (e.g. sending a `Request` to a slave).
    NotAcceptingRequests,
    /// 500 - Other errors.
    InternalServerError,
}

#[derive(Clone, Debug)]
pub struct HttpError {
    pub reason: ErrorReason,
    pub err: String,
}

impl reject::Reject for HttpError {}

impl HttpError {
    pub fn new(reason: ErrorReason, err: String) -> Self {
        HttpError { reason, err }
    }
}

#[derive(Serialize)]
pub struct HttpErrorResponse {
    pub code: u16,
    pub message: String,
}

impl HttpErrorResponse {
    pub fn from_err(val: &HttpError) -> (Self, StatusCode) {
        let code;
        let message;
        match val.reason {
            ErrorReason::Forbidden => {
                code = StatusCode::FORBIDDEN;
                message = val.err.clone();
            }
            ErrorReason::InvalidEncryption => {
                code = StatusCode::UNPROCESSABLE_ENTITY;
                message = val.err.clone();
            }
            ErrorReason::InvalidRequestPayload => {
                code = StatusCode::BAD_REQUEST;
                message = val.err.clone();
            }
            ErrorReason::RateLimit => {
                code = StatusCode::TOO_MANY_REQUESTS;
                message = val.err.clone();
            }
            ErrorReason::SignerNotFound => {
                code = StatusCode::UNAUTHORIZED;
                message = val.err.clone();
            }
            ErrorReason::NotAcceptingRequests => {
                code = StatusCode::MISDIRECTED_REQUEST;
                message = val.err.clone();
            }
            ErrorReason::IllegalNonce => {
                code = StatusCode::PRECONDITION_FAILED;
                message = val.err.clone();
            }

            ErrorReason::InternalServerError => {
                code = StatusCode::INTERNAL_SERVER_ERROR;
                message = format!("{:?} - {}", val.reason, val.err);
            }

            ErrorReason::KycNotFound => {
                code = StatusCode::NOT_FOUND;
                message = val.err.clone();
            }
        }
        (
            HttpErrorResponse {
                code: code.as_u16(),
                message,
            },
            code,
        )
    }
}
