use anyhow::Result;
use async_trait::async_trait;
use deadpool_postgres::{Client, Transaction};
use postgres::{Row, ToStatement};
use postgres_types::ToSql;

/// A trait allowing abstraction over connections and transactions.
///
/// Lets the caller decide whether to execute SQL within a transaction, or directly.
///
/// Behaves like the Strategy pattern and modeled after `tokio_postgres::generic_client`.
#[async_trait]
pub trait TransactionLike {
    async fn query_opt_<T: ?Sized + ToStatement + Sync + Send + ToStatement + Sync + Send>(
        &self,
        query: &T,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<Option<Row>>
    where
        T: ToStatement;

    async fn query_one_<T: ?Sized + ToStatement + Sync + Send + ToStatement + Sync + Send>(
        &self,
        query: &T,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<Row>
    where
        T: ToStatement;

    async fn query_<T: ?Sized + ToStatement + Sync + Send>(
        &self,
        query: &T,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<Vec<Row>>
    where
        T: ToStatement;

    async fn execute_<T: ?Sized + ToStatement + Sync + Send>(
        &self,
        query: &T,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<u64>
    where
        T: ToStatement;
}

#[async_trait]
impl TransactionLike for Client {
    async fn query_opt_<T: ?Sized + ToStatement + Sync + Send>(
        &self,
        query: &T,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<Option<postgres::Row>>
    where
        T: postgres::ToStatement,
    {
        self.query_opt(query, params).await.map_err(|e| e.into())
    }

    async fn query_one_<T: ?Sized + ToStatement + Sync + Send>(
        &self,
        query: &T,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<postgres::Row>
    where
        T: postgres::ToStatement,
    {
        self.query_one(query, params).await.map_err(|e| e.into())
    }

    async fn query_<T: ?Sized + ToStatement + Sync + Send>(
        &self,
        query: &T,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<Vec<Row>>
    where
        T: ToStatement,
    {
        self.query(query, params).await.map_err(|e| e.into())
    }

    async fn execute_<T: ?Sized + ToStatement + Sync + Send>(
        &self,
        query: &T,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<u64>
    where
        T: ToStatement,
    {
        self.execute(query, params).await.map_err(|e| e.into())
    }
}

#[async_trait]
#[allow(clippy::needless_lifetimes)]
impl TransactionLike for Transaction<'_> {
    async fn query_opt_<T: ?Sized + ToStatement + Sync + Send>(
        &self,
        query: &T,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<Option<postgres::Row>>
    where
        T: postgres::ToStatement,
    {
        self.query_opt(query, params).await.map_err(|e| e.into())
    }

    async fn query_one_<T: ?Sized + ToStatement + Sync + Send>(
        &self,
        query: &T,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<postgres::Row>
    where
        T: postgres::ToStatement,
    {
        self.query_one(query, params).await.map_err(|e| e.into())
    }

    async fn query_<T: ?Sized + ToStatement + Sync + Send>(
        &self,
        query: &T,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<Vec<Row>>
    where
        T: ToStatement,
    {
        self.query(query, params).await.map_err(|e| e.into())
    }

    async fn execute_<T: ?Sized + ToStatement + Sync + Send>(
        &self,
        query: &T,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<u64>
    where
        T: ToStatement,
    {
        self.execute(query, params).await.map_err(|e| e.into())
    }
}
