use ddx_common::{
    constants::DEFAULT_PG_POOL_SIZE,
    db::{admin::create_db, make_deadpool},
};
use deadpool_postgres::Pool;
use std::thread;
use tokio::runtime::Runtime;

pub fn get_app_share_dir(app_name: &str) -> String {
    let mut share_dir = std::env::var("APP_SHARE").expect("APP_SHARE not set");
    share_dir.push('/');
    share_dir.push_str(app_name);
    share_dir
}

pub fn setup_db(
    rt: &Runtime,
    db_connstr: &str,
    overwrite: bool,
    sql_name: &str,
    schema_name: &str,
) -> Pool {
    let (cluster_connstr, name) = db_connstr
        .rsplit_once('/')
        .expect("Expected a [Postgres Connection URI](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING) ending with the db name");
    let share_dir = std::env::var("APP_CONFIG").expect("APP_CONFIG not set");
    let connstr = rt
        .block_on(create_db(
            cluster_connstr,
            &share_dir,
            sql_name,
            name,
            schema_name,
            overwrite,
        ))
        .unwrap_or_else(|e| panic!("Failed to create db from {}: {}", schema_name, e));
    make_deadpool(&connstr, DEFAULT_PG_POOL_SIZE)
}

pub fn make_runtime(core_threads: usize) -> tokio::runtime::Runtime {
    tracing::info!("Starting tokio 1 runtime on current thread");
    let mut builder = tokio::runtime::Builder::new_current_thread();
    builder
        // Making sure that basic runtime only use a minimal number of TCS.
        .max_blocking_threads(core_threads)
        .on_thread_start(|| {
            tracing::info!(
                "Current blocking thread tokio 1 started. name: {:?}, id: {:?}",
                thread::current().name(),
                thread::current().id()
            );
        })
        .on_thread_stop(|| {
            tracing::info!(
                "Current worker thread tokio 1 stopped. name: {:?}, id: {:?}",
                thread::current().name(),
                thread::current().id()
            );
        })
        .enable_all();
    builder.build().unwrap()
}
