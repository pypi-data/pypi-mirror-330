use crate::db::txn_like::TransactionLike;
use anyhow::Result;
use serde_json::Value;

pub const KEY_NODE_ID: &str = "NODE_ID";
pub const KEY_STATE_CHECKPOINT: &str = "STATE_CHECKPOINT";

pub async fn get<C: TransactionLike>(client: &C, schema: &str, key: &str) -> Result<Option<Value>> {
    let get_sql = format!(
        "SELECT value FROM {}.internal_state WHERE key = $1 LIMIT 1",
        schema
    );
    let maybe_row = client.query_opt_(&get_sql, &[&key.to_string()]).await?;
    Ok(maybe_row.map(|row| row.get::<_, Value>("value")))
}

pub async fn upsert<C: TransactionLike>(
    txn: &C,
    schema: &str,
    key: &str,
    value: &Value,
) -> Result<u64> {
    let upsert_sql = format!(
        "INSERT INTO {}.internal_state (key, value) VALUES ($1, $2) ON CONFLICT (key) DO UPDATE SET value = $2",
        schema
    );
    txn.execute_(&upsert_sql, &[&key.to_string(), value]).await
}
