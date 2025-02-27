//! The [`ServiceRunner`] in this module is a type that spawns and registers services as defined by the [`Service`] trait.
//!
//! Its goal is to start services using `task::spawn` and provide a unified cancel handle using a oneshot channel. This means that as soon as the oneshot channel is done (it's a [`Future`]), any service run future will be cancelled.

use super::services::{ServiceTask, ServiceWithGracefulShutdown};
use anyhow::{Error, Result, anyhow};
use arc_swap::ArcSwap;
use core::fmt;
use std::{
    collections::BTreeMap,
    sync::{Arc, Mutex},
};
use tokio::{runtime::Handle, sync::oneshot};
use tracing::instrument;
use tracing_futures::Instrument;

enum ServiceStatus {
    Running(oneshot::Sender<()>),
    Failed(Error),
    Stopped,
}

impl std::fmt::Debug for ServiceStatus {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Running(_) => write!(f, "Running"),
            Self::Failed(arg0) => f.debug_tuple("Failed").field(arg0).finish(),
            Self::Stopped => write!(f, "Stopped"),
        }
    }
}

#[derive(thiserror::Error, Debug)]
pub enum ServiceError {
    #[error("Service {name:?} failed with error: {err:?})")]
    ServiceFailed { name: String, err: String },
    #[error("Service {name:?} stopped")]
    ServiceStopped { name: String },
}

#[derive(Clone)]
pub struct ServiceHandle {
    status: Arc<ArcSwap<ServiceStatus>>,
    name: String,
}

impl ServiceHandle {
    pub fn name(&self) -> String {
        self.name.clone()
    }

    #[instrument(level = "info", skip_all, fields(name))]
    pub fn start(name: String, tx: oneshot::Sender<()>) -> Self {
        ServiceHandle {
            status: Arc::new(ArcSwap::from_pointee(ServiceStatus::Running(tx))),
            name,
        }
    }

    fn fail(&self, err: Error) {
        self.status.store(Arc::new(ServiceStatus::Failed(err)));
    }

    #[instrument(level="info", skip_all, fields(name=%self.name))]
    pub fn stop(&self) -> Result<()> {
        let status = self.status.swap(Arc::new(ServiceStatus::Stopped));
        // Assuming this arc has one strong reference because we just took it.
        match Arc::try_unwrap(status).unwrap() {
            ServiceStatus::Running(tx) => tx
                .send(())
                .map_err(|_| anyhow!("Failed to send stop signal")),
            ServiceStatus::Failed(err) => Err(Error::msg(err)),
            ServiceStatus::Stopped => Err(anyhow!("Already stopped")),
        }
    }

    pub fn ensure_running(&self) -> std::result::Result<(), ServiceError> {
        match self.status.load().as_ref() {
            ServiceStatus::Running(_) => Ok(()),
            ServiceStatus::Failed(err) => Err(ServiceError::ServiceFailed {
                name: self.name.clone(),
                err: err.to_string(),
            }),
            ServiceStatus::Stopped => Err(ServiceError::ServiceStopped {
                name: self.name.clone(),
            }),
        }
    }
}

/// A simple runner for [`Service`] implementations.
#[derive(Clone)]
pub struct ServiceRunner {
    runtime: Handle,
    registry: ServiceRegistry,
}

impl fmt::Debug for ServiceRunner {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("ServiceRunner")
            .field("registry", &self.services())
            .finish()
    }
}

impl ServiceRunner {
    /// Provide a [`Handle`] to spawn the [`Service`]s in.
    pub fn with_handle(handle: Handle) -> Self {
        ServiceRunner {
            runtime: handle,
            registry: Default::default(),
        }
    }

    pub fn services(&self) -> Vec<String> {
        self.registry
            .registry
            .lock()
            .unwrap()
            .keys()
            .cloned()
            .collect()
    }

    /// Spawns a tasks that waits for a graceful shutdown signal or failure of the given [`Service`].
    ///
    /// With graceful shutdown, we assume that the service is terminated upon cancelling the runner's future.
    /// Use a different runner for services that await for background components to terminate.
    pub(crate) fn spawn<S: 'static + ServiceTask + Sized + Send>(
        &self,
        service: S,
    ) -> ServiceHandle {
        let (tx, rx) = tokio::sync::oneshot::channel();
        let handle = ServiceHandle::start(service.name(), tx);

        let handle_ = handle.clone();
        let service_name = service.name();
        let execution_future = async move {
            let service_name = service.name();
            tokio::select! {
                res = service.run() => {
                    // Unwrapping the task result from the join handle.
                    let err = res.err().unwrap_or_else(|| anyhow!("Service {} interrupted", service_name));
                    tracing::error!(%err, "Failure");
                    handle_.fail(err);
                }
                _ = rx => {
                    tracing::info!("Shut down gracefully");
                }
            }
        };
        {
            let _guard = self.runtime.enter();
            tokio::task::Builder::new()
                .name(format!("{} service runner", service_name).as_str())
                .spawn(execution_future.instrument(tracing::debug_span!("spawn", %service_name)))
                .unwrap();
        }
        tracing::info!(%service_name, ">spawned");
        handle
    }

    pub fn spawn_and_register<S: 'static + ServiceTask + Sized + Send>(&self, service: S) {
        let handle = self.spawn(service);
        self.registry.register(handle);
    }

    /// Spawn a service with a graceful shutdown routine
    ///
    /// Instead of dropping the service task on shutdown, this runner expects the service to
    /// handle a shutdown receiver to end its task.
    pub fn spawn_with_graceful_shutdown<S: 'static + ServiceWithGracefulShutdown + Sized + Send>(
        &self,
        service: S,
    ) -> ServiceHandle {
        let (tx, rx) = tokio::sync::oneshot::channel();
        let handle = ServiceHandle::start(service.name(), tx);

        let service_name = service.name();
        let execution_future = service.run(rx);
        {
            let _guard = self.runtime.enter();
            tokio::task::Builder::new()
                .name(format!("{} service runner", service_name).as_str())
                .spawn(execution_future.instrument(tracing::debug_span!("spawn", %service_name)))
                .unwrap();
        }
        tracing::info!(%service_name, ">spawned with graceful shutdown");
        handle
    }

    pub fn spawn_with_graceful_shutdown_and_register<
        S: 'static + ServiceWithGracefulShutdown + Sized + Send,
    >(
        &self,
        service: S,
    ) {
        let handle = self.spawn_with_graceful_shutdown(service);
        self.registry.register(handle);
    }

    pub fn ensure_running(&self) -> std::result::Result<(), ServiceError> {
        self.registry.ensure_running()
    }

    #[tracing::instrument(level = "info", skip_all)]
    pub fn shutdown(&self) -> Result<()> {
        self.registry.shutdown(&[])
    }

    #[tracing::instrument(level = "info", skip(self))]
    pub fn shutdown_services(&self, services: &[String]) -> Result<()> {
        let exclude = {
            let registry = self.registry.registry.lock().unwrap();
            registry
                .keys()
                .filter(|k| services.contains(k))
                .cloned()
                .collect::<Vec<_>>()
        };
        self.registry.shutdown(&exclude)
    }

    /// Deregister a list of services from the runner so that node health monitor will not check them.
    ///
    /// They will not be shut down gracefully.
    pub fn deregister_services(&self, services: &[String]) {
        for s in services {
            self.registry.deregister(s);
        }
    }
}

/// A non-exhaustive list of services to shut down in their logical shut down order.
const SHUTDOWN_SEQUENCE: &[&str] = &[
    "NodeHealthMonitor",
    "PriceFeed",
    "CacheManager",
    "DbBackupManager",
    "MembershipManager",
    "ElectionReactor",
    "MonotonicClock",
    "BlockProducer",
    "BlockWatcher",
    "ApiService",
];

/// A simple service registry to store [`ServiceHandle`]s with their name.
#[derive(Default, Clone)]
struct ServiceRegistry {
    /// A map of service handles
    registry: Arc<Mutex<BTreeMap<String, ServiceHandle>>>,
}

impl ServiceRegistry {
    pub fn register(&self, handle: ServiceHandle) {
        self.registry.lock().unwrap().insert(handle.name(), handle);
    }

    pub fn deregister(&self, name: &String) {
        self.registry.lock().unwrap().remove(name);
    }

    /// Shuts down the given services
    ///
    /// An empty filter will shut down all services
    #[tracing::instrument(level = "debug", skip(self))]
    pub fn shutdown(&self, exclude: &[String]) -> Result<()> {
        // Using a copy to eliminate the possibility deadlock during the shutdown routine
        let mut new_registry = {
            let registry = self.registry.lock().unwrap();
            let mut sorted_values: Vec<(String, ServiceHandle)> =
                Vec::with_capacity(registry.len());
            // Sort the services according to the shutdown sequence for good measure.
            // Normally, there should not be inter-dependencies between services.
            for name in SHUTDOWN_SEQUENCE.iter().map(ToString::to_string) {
                if let Some(handle) = registry.get(&name) {
                    sorted_values.push((name, handle.clone()));
                }
            }
            // Add remaining services in the end if the shutdown sequence is not complete.
            // The registry keeps services sorted alphabetically to avoid any randomness in the shutdown sequence.
            if sorted_values.len() < registry.len() {
                for (name, handle) in registry.iter() {
                    if !sorted_values.iter().any(|(n, _)| n == name) {
                        sorted_values.push((name.clone(), handle.clone()));
                    }
                }
            }
            sorted_values
        };
        let stopped = new_registry
            .extract_if(|(service, handle)| {
                if !exclude.contains(service) {
                    if let Err(reason) = handle.stop() {
                        tracing::error!(%service, ?reason, "Failed to shut down");
                        false
                    } else {
                        true
                    }
                } else {
                    false
                }
            })
            .map(|(name, _)| name)
            .collect::<Vec<_>>();
        tracing::info!(?stopped, "DONE shutting down services");
        let mut registry = self.registry.lock().unwrap();
        *registry = new_registry.into_iter().collect();
        if !registry.is_empty() {
            tracing::info!(running=?registry.keys(), "Services still running")
        }
        Ok(())
    }

    pub fn ensure_running(&self) -> std::result::Result<(), ServiceError> {
        // Check that all services registered are still running
        for (_name, handle) in self.registry.lock().unwrap().iter() {
            handle.ensure_running()?
        }
        Ok(())
    }
}
