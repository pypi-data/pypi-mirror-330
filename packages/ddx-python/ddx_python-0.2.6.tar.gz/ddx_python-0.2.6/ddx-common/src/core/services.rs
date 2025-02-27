use crate::types::transaction::{Event, Tx};
use anyhow::Result;
use rust_decimal::Decimal;
use serde::Serialize;
use std::{
    collections::{BTreeMap, HashMap},
    fmt, mem,
    time::Duration,
};
use tokio::{
    select,
    sync::{Mutex, mpsc::Sender, oneshot},
    task::JoinHandle,
};

pub type TxLogBroadcastReceiver = tokio::sync::broadcast::Receiver<Tx<Event>>;

/// Formalizes a services by wrapping the Tokio task with metadata and lifecycle.
///
/// Services include: EthBlockWatcher, BlockProducer, MonotonicClock, Webserver, MembershipManager, SnapshotManager and PriceFeed
#[async_trait::async_trait]
pub trait Service {
    /// A service's name. Will be used for logging (and other stuff).
    fn name(&self) -> String;
}

/// Service encapsulated in a `tokio::task`
#[async_trait::async_trait]
pub trait ServiceTask: Service {
    /// Runs the service. await for foreground
    async fn run(self) -> Result<()>;
}

/// Service encapsulated in a `tokio::task` with a shutdown interrupt
#[async_trait::async_trait]
pub trait ServiceWithGracefulShutdown: Service {
    /// Runs the service on the foreground until the given shutdown interrupts it
    ///
    /// The service logic must handle the shutdown signal to shut down gracefully.
    /// Use the `Service` trait for a more generic variant that simply drops the runner future.
    async fn run(self, shutdown: oneshot::Receiver<()>) -> Result<()>;
}

#[async_trait::async_trait]
pub trait TxLogSubscriber {
    /// Subscribe to the provided [`TxLogStream`].
    async fn subscribe(&mut self, tx_log: TxLogBroadcastReceiver);
}

pub trait ServiceEvent {
    /// Creates a group by key
    fn as_group_key(&self) -> String;
}

pub trait ServiceEventWithDuration {
    fn elapsed(&self) -> Duration;
}

pub const LOG_DRAIN_INTERVAL_IN_SECS: u64 = 5;

#[derive(Default, Serialize)]
pub struct AvgDurationMetric {
    pub count: u64,
    pub avg_elapsed: String,
}

impl AvgDurationMetric {
    pub fn new(count: u64, durations: Vec<Duration>) -> Self {
        AvgDurationMetric {
            count,
            // Use a format consistent with tracing's durations.
            avg_elapsed: format!(
                "{}ms",
                Decimal::from_i128_with_scale(
                    durations
                        .into_iter()
                        .sum::<Duration>()
                        .div_f64(count as f64)
                        .as_micros() as i128,
                    3,
                )
                .round_dp(2)
                .normalize(),
            ),
        }
    }
}

#[derive(Default, Serialize)]
struct EventLogMetricsWithDuration {
    count: usize,
    groups: BTreeMap<String, AvgDurationMetric>,
}

impl EventLogMetricsWithDuration {
    #[tracing::instrument(level = "debug", skip_all)]
    pub fn fold_metrics<E>(events: &mut Vec<E>) -> Self
    where
        E: fmt::Debug + Serialize + ServiceEvent + ServiceEventWithDuration,
    {
        let mut items: HashMap<String, (u64, Vec<Duration>)> = Default::default();
        let count;
        {
            count = events.len();
            for evt in events.drain(..) {
                let entry = items.entry(evt.as_group_key()).or_default();
                entry.0 += 1;
                entry.1.push(evt.elapsed());
            }
        }
        EventLogMetricsWithDuration {
            count,
            groups: items
                .into_iter()
                .map(|(k, m)| (k, AvgDurationMetric::new(m.0, m.1)))
                .collect(),
        }
    }
}

pub struct EventLogHandle {
    shutdown_tx: oneshot::Sender<()>,
    t_handle: JoinHandle<()>,
}

impl EventLogHandle {
    pub async fn shutdown(self) -> Result<()> {
        self.shutdown_tx
            .send(())
            .map_err(|_e| anyhow::Error::msg("Shutdown Error"))?;
        let _ = self.t_handle.await;
        Ok(())
    }
}

/// Trait to record events into a log with durations
///
/// These logs are emitted by tracing, which can then be processed by the as metrics by the event-driven logging middleware.
///
/// We use a channel patter to send the log from the service to a collection task. Compared to the locking sync primitive
/// alternative, this mitigates risks of contention form frequent locks from multiple threads. It also helps performance
/// by enabling a wait free `record` (within the channels bounds) via batching.
#[async_trait::async_trait]
pub trait EventLogWithDurations<
    E: 'static + fmt::Debug + Serialize + ServiceEvent + ServiceEventWithDuration + Send + Sync,
>: Service
{
    /// Send the given event to the log collector
    ///
    /// This is a non-blocking operation, the event is batched and sent to the collector via a channel.
    /// Events are dequeued before processing, so reaching the channel bounds indicates internal malfunction.
    #[tracing::instrument(level = "trace", skip_all, fields(?event))]
    fn record(&self, event: E) -> Result<()> {
        if let Some(tx) = self.tx_ref() {
            tx.try_send(event).map_err(anyhow::Error::new)
        } else {
            Err(anyhow::Error::msg("Log sender not initialized".to_string()))
        }
    }

    fn init_log(&mut self, tx: Sender<E>);

    /// Gets a reference to the log sender
    fn tx_ref(&self) -> &Option<Sender<E>>;

    /// Spawns a log draining and folding scheduler task
    ///
    /// This should be called only once per service, normally as part of the `run` routine.
    async fn spawn_log(&mut self) -> EventLogHandle {
        let (shutdown_tx, shutdown_rx) = oneshot::channel::<()>();
        // The channel is bounded for good measure, events are being actively dequeued so should not accumulate in a functioning system.
        let (tx, mut rx) = tokio::sync::mpsc::channel(10000);
        self.init_log(tx);
        let service_name = self.name();
        let t_handle = tokio::task::spawn(async move {
            // Each async block returns to the executor so this has to be thread safe.
            // However, this pattern mitigates risks of contention by reducing locks to a minimum with batch updates.
            let events = Mutex::new(vec![]);
            let collector = async {
                while let Some(event) = rx.recv().await {
                    tracing::trace!(?event, "Dequeued");
                    events.lock().await.push(event);
                }
            };
            let scheduler = async {
                let mut interval =
                    tokio::time::interval(Duration::from_secs(LOG_DRAIN_INTERVAL_IN_SECS));
                interval.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Skip);
                loop {
                    let mut guard = events.lock().await;
                    // Tracing dispatches a log event on close, nothing else to do with the metric.
                    let EventLogMetricsWithDuration { count, groups } =
                        EventLogMetricsWithDuration::fold_metrics(&mut guard);
                    if count > 0 {
                        tracing::debug!(metric_name="event_log", %service_name, %count, groups=%serde_json::to_string(&groups).unwrap(), "Scheduled summary");
                    }
                    mem::drop(guard);
                    tracing::debug!("Waiting for next tick to fold log events");
                    interval.tick().await;
                }
            };
            select! {
                _ = collector => {
                    tracing::warn!("Log collector exited early");
                }
                _ = scheduler => {
                    tracing::warn!("Log scheduler exited early");
                }
                _ = shutdown_rx => {
                    // Logs the remaining access log before shutting down to avoid incomplete log.
                    let mut guard = events.lock().await;
                    let EventLogMetricsWithDuration { count, groups } =
                        EventLogMetricsWithDuration::fold_metrics(&mut guard);
                    tracing::info!(metric_name="event_log", %service_name, %count, groups=%serde_json::to_string(&groups).unwrap(), "Last summary before shutdown");
                }
            }
        });
        EventLogHandle {
            shutdown_tx,
            t_handle,
        }
    }
}
