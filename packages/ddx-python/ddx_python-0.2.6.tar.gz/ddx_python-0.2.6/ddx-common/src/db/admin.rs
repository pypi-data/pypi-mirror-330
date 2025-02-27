use anyhow::Result;
use std::path::PathBuf;

pub fn env_pg_cluster() -> String {
    std::env::var("PG_CLUSTER").expect("PG_CLUSTER is required by all runtime modes using a db")
}

/// Creates the db by loading a sql file and executing it.
pub async fn create_db(
    cluster_connstr: &str,
    share_dir: &str,
    sql_filename: &str,
    db_name: &str,
    schema_name: &str,
    overwrite: bool,
) -> Result<String> {
    let config = cluster_connstr.parse::<tokio_postgres::Config>()?;
    let connstr = format!("{}/{}", cluster_connstr, db_name);
    let (client, conn) = config.connect(tokio_postgres::NoTls).await?;
    tokio::spawn(conn);
    let row = client
        .query_opt(
            "SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower($1);",
            &[&db_name],
        )
        .await?;
    tracing::trace!(exists=?row.is_some(), "Db lookup");
    if row.is_some() && !overwrite {
        tracing::trace!(%connstr, "Using existing db");
        return Ok(connstr);
    }
    // Create a pristine db, dropping existing if exists.
    let changes = client
        .execute(
            format!("DROP DATABASE IF EXISTS {};", db_name).as_str(),
            &[],
        )
        .await?;
    tracing::trace!(?changes, "Dropped db");
    let changes = client
        .execute(format!("CREATE DATABASE {};", db_name).as_str(), &[])
        .await?;
    tracing::trace!(?changes, "Created db");
    let changes = client
        .execute(
            format!(
                "ALTER DATABASE {} SET search_path = {};",
                db_name, schema_name
            )
            .as_str(),
            &[],
        )
        .await?;
    tracing::trace!(?changes, "Set default search path");
    let config = connstr.parse::<tokio_postgres::Config>()?;
    // Execution sql file in the new db.
    let (client, conn) = config.connect(tokio_postgres::NoTls).await?;
    tokio::spawn(conn);

    let mut migrations_path = PathBuf::from(&share_dir);
    migrations_path.push("sql");
    migrations_path.push(sql_filename);

    let sql = tokio::fs::read_to_string(&migrations_path).await?;
    client.batch_execute(&sql).await?;
    tracing::debug!(?migrations_path, "KYC SQL script executed successfully");
    Ok(connstr)
}
