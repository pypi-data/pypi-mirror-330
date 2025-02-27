use deadpool_postgres::{Manager, ManagerConfig, RecyclingMethod};
use std::time::Duration;

pub mod admin;
pub mod txn_like;

const DEADPOOL_TIMEOUT: Duration = Duration::from_secs(60 * 30);

#[tracing::instrument(level = "info", skip(max_size))]
pub fn make_deadpool(connstr: &str, max_size: usize) -> deadpool_postgres::Pool {
    let mut config = connstr.parse::<tokio_postgres::Config>().unwrap();
    config.connect_timeout(DEADPOOL_TIMEOUT);
    let manager_config = ManagerConfig {
        // Only run `Client::is_closed` when recycling existing connections.
        // Revisit this config if experiencing any stale connection issue.
        recycling_method: RecyclingMethod::Fast,
    };
    let mgr = Manager::from_config(config, tokio_postgres::NoTls, manager_config);
    // An async connection pool
    deadpool_postgres::Pool::builder(mgr)
        .max_size(max_size)
        .build()
        .expect("Couldn't build connection pool")
}
