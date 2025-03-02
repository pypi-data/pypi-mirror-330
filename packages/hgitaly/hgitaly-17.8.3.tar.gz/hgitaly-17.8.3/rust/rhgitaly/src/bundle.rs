// Copyright 2025 Georges Racinet <georges.racinet@octobus.net>
//
// This software may be used and distributed according to the terms of the
// GNU General Public License version 2 or any later version.
// SPDX-License-Identifier: GPL-2.0-or-later

use std::ffi::OsString;
use std::fmt::{Debug, Formatter};
use std::path::PathBuf;
use std::sync::Arc;
use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;
use tokio_util::sync::CancellationToken;
use tonic::{metadata::MetadataMap, Response, Status};
use tracing::{debug, info, warn};

use crate::config::Config;
use crate::gitaly::{
    CreateBundleRequest, CreateBundleResponse, CreateRepositoryFromBundleRequest, Repository,
};
use crate::repository::spawner::{BytesChunking, RepoProcessSpawnerTemplate};
use crate::repository::{RequestWithBytesChunk, RequestWithRepo};
use crate::streaming::{ResultResponseStream, WRITE_BUFFER_SIZE};

/// In this function, the Repository is assumed to be a Git repository,
/// sitting exacly at the given relative path (no switch to hg, no diversion to +hgitaly area)
pub async fn create_git_bundle(
    config: Arc<Config>,
    repo_path: PathBuf,
    shutdown_token: CancellationToken,
    metadata: &MetadataMap,
) -> ResultResponseStream<CreateBundleResponse> {
    let git_config = Vec::new();
    let spawner_tmpl = RepoProcessSpawnerTemplate::new_git_at_path(
        config.clone(),
        repo_path,
        metadata,
        git_config,
    )
    .await?;
    let mut spawner = spawner_tmpl.git_spawner();
    // TODO evaluate needs for buffers? One can expect RHGitaly to read it fast
    // unless all threads are busy.
    let (stdout_tx, mut stdout_rx) = mpsc::channel(3);
    spawner.capture_stdout(stdout_tx, BytesChunking::Binary(*WRITE_BUFFER_SIZE));
    let args: Vec<OsString> = vec!["bundle".into(), "create".into(), "-".into(), "--all".into()];
    spawner.args(&args);

    let (tx, rx) = mpsc::channel(1);
    let spawned = spawner.spawn(shutdown_token);
    let tx2 = tx.clone();

    let read_stdout = async move {
        while let Some(data) = stdout_rx.recv().await {
            debug!("Received {} bytes", data.len());
            tx.send(Ok(CreateBundleResponse { data }))
                .await
                .unwrap_or_else(|e| {
                    warn!(
                        "Request cancelled by client before all results \
                             could be streamed back: {e}"
                    )
                })
        }
        info!("Finished listening on internal channel for bundle data");
    };

    tokio::task::spawn(async move {
        let spawn_result = tokio::join!(spawned, read_stdout).0;
        let err = match spawn_result {
            Ok(0) => return,
            Ok(git_exit_code) => {
                Status::internal(format!("Git subprocess exited with code {}", git_exit_code))
            }
            Err(e) => e,
        };

        if tx2.send(Err(err.clone())).await.is_err() {
            warn!("Request cancelled by client before error {err:?} could be streamed back");
        }
    });

    Ok(Response::new(Box::pin(ReceiverStream::new(rx))))
}

pub async fn create_repo_from_git_bundle(
    config: Arc<Config>,
    repo_path: PathBuf,
    bundle_path: PathBuf,
    shutdown_token: CancellationToken,
    metadata: &MetadataMap,
) -> Result<(), Status> {
    let git_config = vec![
        // See comment in FetchBundle
        ("transfer.fsckObjects".into(), "false".into()),
    ];

    let cwd = config.repositories_root.clone();

    let mut spawner =
        RepoProcessSpawnerTemplate::new_git_at_path(config, cwd, metadata, git_config)
            .await?
            .git_spawner();

    let args: Vec<OsString> = vec![
        "clone".into(),
        "--bare".into(),
        "--quiet".into(),
        bundle_path.into(),
        repo_path.into(),
    ];
    spawner.args(&args);
    info!("Git args: {:?}", &args);
    let git_exit_code = spawner.spawn(shutdown_token).await?;
    if git_exit_code != 0 {
        warn!("Git subprocess exited with code {git_exit_code}");
        return Err(Status::internal(format!(
            "Git subprocess exited with code {git_exit_code}"
        )));
    }
    Ok(())
}

pub struct CreateBundleTracingRequest<'a>(pub &'a CreateBundleRequest);

impl Debug for CreateBundleTracingRequest<'_> {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("CreateBundle")
            .field("repository", &self.0.repository)
            .finish()
    }
}

impl RequestWithRepo for CreateBundleRequest {
    fn repository_ref(&self) -> Option<&Repository> {
        self.repository.as_ref()
    }
}

pub struct CreateRepositoryFromBundleTracingRequest<'a>(pub &'a CreateRepositoryFromBundleRequest);

impl Debug for CreateRepositoryFromBundleTracingRequest<'_> {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("CreateRepositoryFromBundle")
            .field("repository", &self.0.repository)
            .finish()
    }
}

impl RequestWithRepo for CreateRepositoryFromBundleRequest {
    fn repository_ref(&self) -> Option<&Repository> {
        self.repository.as_ref()
    }
}

impl RequestWithBytesChunk for CreateRepositoryFromBundleRequest {
    fn bytes_chunk(&self) -> &[u8] {
        &self.data
    }
}
