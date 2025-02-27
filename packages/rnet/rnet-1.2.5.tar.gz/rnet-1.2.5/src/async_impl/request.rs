use crate::apply_option;
use crate::{
    async_impl::{Response, WebSocket},
    error::wrap_rquest_error,
    param::{RequestParams, WebSocketParams},
    types::{Method, Version},
    Result,
};
use pyo3::prelude::*;
use rquest::redirect::Policy;
use std::ops::Deref;
use std::{sync::Arc, time::Duration};

/// Executes an HTTP request.
pub async fn execute_request<C, U>(
    client: C,
    method: Method,
    url: U,
    mut params: Option<RequestParams>,
) -> Result<Response>
where
    C: Deref<Target = rquest::Client>,
    U: AsRef<str>,
{
    let params = params.get_or_insert_default();
    let mut builder = client.request(method.into_ffi(), url.as_ref());

    // Version options.
    apply_option!(
        apply_transformed_option,
        builder,
        params.version,
        version,
        Version::into_ffi
    );

    // Allow redirects options.
    apply_option!(
        apply_option_or_default_with_value,
        builder,
        params.allow_redirects,
        redirect,
        false,
        params
            .max_redirects
            .take()
            .map(Policy::limited)
            .unwrap_or_default()
    );

    // Timeout options.
    apply_option!(
        apply_transformed_option,
        builder,
        params.timeout,
        timeout,
        Duration::from_secs
    );
    apply_option!(
        apply_transformed_option,
        builder,
        params.read_timeout,
        read_timeout,
        Duration::from_secs
    );

    // Network options.
    apply_option!(apply_if_some, builder, params.proxy, proxy);
    apply_option!(apply_if_some, builder, params.local_address, local_address);
    rquest::cfg_bindable_device!(
        apply_option!(apply_if_some, builder, params.interface, interface);
    );

    // Headers options.
    if let Some(headers) = params.headers.take() {
        for (key, value) in headers {
            builder = builder.header(key, value);
        }
    }

    // Authentication options.
    apply_option!(apply_if_some, builder, params.auth, auth);

    // Bearer authentication options.
    apply_option!(apply_if_some, builder, params.bearer_auth, bearer_auth);

    // Basic authentication options.
    if let Some(basic_auth) = params.basic_auth.take() {
        builder = builder.basic_auth(basic_auth.0, basic_auth.1);
    }

    // Query options.
    apply_option!(apply_if_some_ref, builder, params.query, query);

    // Form options.
    apply_option!(apply_if_some_ref, builder, params.form, form);

    // JSON options.
    apply_option!(apply_if_some_ref, builder, params.json, json);

    // Body options.
    apply_option!(apply_if_some, builder, params.body, body);

    // Multipart options.
    if let Some(multipart) = params.multipart.take() {
        let multipart = Python::with_gil(|py| multipart.borrow_mut(py).0.take());
        if let Some(multipart) = multipart {
            builder = builder.multipart(multipart);
        }
    }

    // Send the request.
    builder
        .send()
        .await
        .map(Response::new)
        .map_err(wrap_rquest_error)
}

/// Executes a WebSocket request.
pub async fn execute_websocket_request<C, U>(
    client: C,
    url: U,
    mut params: Option<WebSocketParams>,
) -> Result<WebSocket>
where
    C: Deref<Target = rquest::Client>,
    U: AsRef<str>,
{
    let params = params.get_or_insert_default();
    let mut builder = client.websocket(url.as_ref());

    // The protocols to use for the request.
    apply_option!(apply_if_some, builder, params.protocols, protocols);

    // The WebSocket config
    apply_option!(
        apply_if_some,
        builder,
        params.write_buffer_size,
        write_buffer_size
    );
    apply_option!(
        apply_if_some,
        builder,
        params.max_write_buffer_size,
        max_write_buffer_size
    );
    apply_option!(
        apply_if_some,
        builder,
        params.max_frame_size,
        max_frame_size
    );
    apply_option!(
        apply_if_some,
        builder,
        params.max_message_size,
        max_message_size
    );
    apply_option!(
        apply_if_some,
        builder,
        params.accept_unmasked_frames,
        accept_unmasked_frames
    );

    // The origin to use for the request.
    builder = builder.with_builder(|mut builder| {
        // Network options.
        apply_option!(apply_if_some, builder, params.proxy, proxy);
        apply_option!(apply_if_some, builder, params.local_address, local_address);
        rquest::cfg_bindable_device!(
            apply_option!(apply_if_some, builder, params.interface, interface);
        );

        // Authentication options.
        apply_option!(apply_if_some, builder, params.auth, auth);

        // Bearer authentication options.
        apply_option!(apply_if_some, builder, params.bearer_auth, bearer_auth);

        // Basic authentication options.
        if let Some(basic_auth) = params.basic_auth.take() {
            builder = builder.basic_auth(basic_auth.0, basic_auth.1);
        }

        // Headers options.
        if let Some(headers) = params.headers.take() {
            for (key, value) in headers {
                builder = builder.header(key, value);
            }
        }

        // Query options.
        apply_option!(apply_if_some_ref, builder, params.query, query);

        builder
    });

    WebSocket::new(builder).await
}

/// Executes an HTTP request.
#[inline(always)]
pub async fn execute_request2<C, U>(
    client: C,
    method: Method,
    url: U,
    params: Option<RequestParams>,
) -> Result<Response>
where
    C: Deref<Target = Arc<rquest::Client>>,
    U: AsRef<str>,
{
    let client = client.deref().deref();
    execute_request(client, method, url, params).await
}

/// Executes a WebSocket request.
#[inline(always)]
pub async fn execute_websocket_request2<C, U>(
    client: C,
    url: U,
    params: Option<WebSocketParams>,
) -> Result<WebSocket>
where
    C: Deref<Target = Arc<rquest::Client>>,
    U: AsRef<str>,
{
    let client = client.deref().deref();
    execute_websocket_request(client, url, params).await
}
