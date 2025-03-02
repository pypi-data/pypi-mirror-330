// Copyright 2023 Georges Racinet <georges.racinet@octobus.net>
//
// This software may be used and distributed according to the terms of the
// GNU General Public License version 2 or any later version.
// SPDX-License-Identifier: GPL-2.0-or-later
use crate::gitaly::server_service_server::{ServerService, ServerServiceServer};
use crate::gitaly::{ServerInfoRequest, ServerInfoResponse};
use tonic::{Request, Response, Status};
use tracing::{info, instrument};

build_const!("constants");

#[derive(Debug, Default)]
pub struct ServerServiceImpl {}

#[tonic::async_trait]
impl ServerService for ServerServiceImpl {
    #[instrument]
    async fn server_info(
        &self,
        _request: Request<ServerInfoRequest>,
    ) -> Result<Response<ServerInfoResponse>, Status> {
        info!("Processing");
        Ok(Response::new(ServerInfoResponse {
            server_version: HGITALY_VERSION.into(),
            ..Default::default()
        }))
    }
}

/// Takes care of boilerplate that would instead be in the startup sequence.
pub fn server_server() -> ServerServiceServer<ServerServiceImpl> {
    ServerServiceServer::new(ServerServiceImpl::default())
}
