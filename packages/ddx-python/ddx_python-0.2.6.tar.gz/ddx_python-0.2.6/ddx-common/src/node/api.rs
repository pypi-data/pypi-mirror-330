use super::errors::{HttpError, HttpErrorResponse};
use crate::core::services::AvgDurationMetric;
use reqwest::StatusCode;
use serde::Serialize;
use std::{
    collections::{BTreeMap, HashMap},
    convert::Infallible,
    sync::{Arc, Mutex},
    time::Duration,
};
use warp::{Filter, http};

pub const ACCESS_LOG_DRAIN_INTERVAL_IN_SECS: u64 = 5;

#[derive(Debug)]
pub struct AccessEvent {
    pub method: http::Method,
    pub route: String,
    pub status: http::StatusCode,
    pub elapsed: Duration,
}

pub type RouteName = String;
pub type HttpStatusCode = u16;

#[derive(Default, Serialize)]
pub struct AccessLogMetric(BTreeMap<RouteName, BTreeMap<HttpStatusCode, AvgDurationMetric>>);

impl AccessLogMetric {
    #[tracing::instrument(level = "debug", skip_all, fields(count, by_route))]
    pub fn fold_access_log(events: &Arc<Mutex<Vec<AccessEvent>>>) -> Self {
        let mut items: HashMap<String, HashMap<u16, (u64, Vec<Duration>)>> = Default::default();
        {
            let mut events = events.lock().unwrap();
            tracing::Span::current().record("count", events.len().to_string());
            for evt in events.drain(..) {
                let route = items.entry(evt.route).or_default();
                let entry = route.entry(evt.status.as_u16()).or_default();
                entry.0 += 1;
                entry.1.push(evt.elapsed);
            }
        }
        // Dispatch info log if any access event took place.
        let by_route = AccessLogMetric(
            items
                .into_iter()
                .map(|(r, v)| {
                    (
                        r,
                        v.into_iter()
                            .map(|(k, m)| (k, AvgDurationMetric::new(m.0, m.1)))
                            .collect::<BTreeMap<_, _>>(),
                    )
                })
                .collect(),
        );
        tracing::Span::current().record("by_route", serde_json::to_string(&by_route).unwrap());
        by_route
    }
}

/// Adds an additional argument to the request handler
pub fn with_cloned<T: Clone + Send>(
    state: T,
) -> impl Filter<Extract = (T,), Error = Infallible> + Clone {
    warp::any().map(move || state.clone())
}

/// Maps our application error type to HTTP error codes instead of just raising 500 errors.
///
/// This includes a JSON representation of the code and message in the response body.
pub async fn handle_rejection(err: warp::Rejection) -> Result<impl warp::Reply, Infallible> {
    let (response, code) = if let Some(http_err) = err.find::<HttpError>() {
        HttpErrorResponse::from_err(http_err)
    } else {
        let code = StatusCode::INTERNAL_SERVER_ERROR;
        (
            HttpErrorResponse {
                code: code.as_u16(),
                message: "Unhandled Rejection".to_string(),
            },
            code,
        )
    };

    Ok(warp::reply::with_status(warp::reply::json(&response), code))
}
