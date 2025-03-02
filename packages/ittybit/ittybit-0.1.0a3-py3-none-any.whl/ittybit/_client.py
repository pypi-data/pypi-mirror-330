# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from .resources import logs, files, media, tasks, events, projects, webhooks, automations
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import IttybitError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Ittybit", "AsyncIttybit", "Client", "AsyncClient"]


class Ittybit(SyncAPIClient):
    automations: automations.AutomationsResource
    files: files.FilesResource
    logs: logs.LogsResource
    events: events.EventsResource
    media: media.MediaResource
    projects: projects.ProjectsResource
    tasks: tasks.TasksResource
    webhooks: webhooks.WebhooksResource
    with_raw_response: IttybitWithRawResponse
    with_streaming_response: IttybitWithStreamedResponse

    # client options
    api_key: str
    accept_version: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        accept_version: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous ittybit client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `API_KEY`
        - `accept_version` from `ACCEPT_VERSION`
        """
        if api_key is None:
            api_key = os.environ.get("API_KEY")
        if api_key is None:
            raise IttybitError(
                "The api_key client option must be set either by passing api_key to the client or by setting the API_KEY environment variable"
            )
        self.api_key = api_key

        if accept_version is None:
            accept_version = os.environ.get("ACCEPT_VERSION")
        if accept_version is None:
            raise IttybitError(
                "The accept_version client option must be set either by passing accept_version to the client or by setting the ACCEPT_VERSION environment variable"
            )
        self.accept_version = accept_version

        if base_url is None:
            base_url = os.environ.get("ITTYBIT_BASE_URL")
        if base_url is None:
            base_url = f"https://api.ittybit.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.automations = automations.AutomationsResource(self)
        self.files = files.FilesResource(self)
        self.logs = logs.LogsResource(self)
        self.events = events.EventsResource(self)
        self.media = media.MediaResource(self)
        self.projects = projects.ProjectsResource(self)
        self.tasks = tasks.TasksResource(self)
        self.webhooks = webhooks.WebhooksResource(self)
        self.with_raw_response = IttybitWithRawResponse(self)
        self.with_streaming_response = IttybitWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        if self._api_key_auth:
            return self._api_key_auth
        if self._accept_version:
            return self._accept_version
        return {}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": api_key}

    @property
    def _accept_version(self) -> dict[str, str]:
        accept_version = self.accept_version
        return {"Accept-Version": accept_version}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        accept_version: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            accept_version=accept_version or self.accept_version,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncIttybit(AsyncAPIClient):
    automations: automations.AsyncAutomationsResource
    files: files.AsyncFilesResource
    logs: logs.AsyncLogsResource
    events: events.AsyncEventsResource
    media: media.AsyncMediaResource
    projects: projects.AsyncProjectsResource
    tasks: tasks.AsyncTasksResource
    webhooks: webhooks.AsyncWebhooksResource
    with_raw_response: AsyncIttybitWithRawResponse
    with_streaming_response: AsyncIttybitWithStreamedResponse

    # client options
    api_key: str
    accept_version: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        accept_version: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async ittybit client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `API_KEY`
        - `accept_version` from `ACCEPT_VERSION`
        """
        if api_key is None:
            api_key = os.environ.get("API_KEY")
        if api_key is None:
            raise IttybitError(
                "The api_key client option must be set either by passing api_key to the client or by setting the API_KEY environment variable"
            )
        self.api_key = api_key

        if accept_version is None:
            accept_version = os.environ.get("ACCEPT_VERSION")
        if accept_version is None:
            raise IttybitError(
                "The accept_version client option must be set either by passing accept_version to the client or by setting the ACCEPT_VERSION environment variable"
            )
        self.accept_version = accept_version

        if base_url is None:
            base_url = os.environ.get("ITTYBIT_BASE_URL")
        if base_url is None:
            base_url = f"https://api.ittybit.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.automations = automations.AsyncAutomationsResource(self)
        self.files = files.AsyncFilesResource(self)
        self.logs = logs.AsyncLogsResource(self)
        self.events = events.AsyncEventsResource(self)
        self.media = media.AsyncMediaResource(self)
        self.projects = projects.AsyncProjectsResource(self)
        self.tasks = tasks.AsyncTasksResource(self)
        self.webhooks = webhooks.AsyncWebhooksResource(self)
        self.with_raw_response = AsyncIttybitWithRawResponse(self)
        self.with_streaming_response = AsyncIttybitWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        if self._api_key_auth:
            return self._api_key_auth
        if self._accept_version:
            return self._accept_version
        return {}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": api_key}

    @property
    def _accept_version(self) -> dict[str, str]:
        accept_version = self.accept_version
        return {"Accept-Version": accept_version}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        accept_version: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            accept_version=accept_version or self.accept_version,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class IttybitWithRawResponse:
    def __init__(self, client: Ittybit) -> None:
        self.automations = automations.AutomationsResourceWithRawResponse(client.automations)
        self.files = files.FilesResourceWithRawResponse(client.files)
        self.logs = logs.LogsResourceWithRawResponse(client.logs)
        self.events = events.EventsResourceWithRawResponse(client.events)
        self.media = media.MediaResourceWithRawResponse(client.media)
        self.projects = projects.ProjectsResourceWithRawResponse(client.projects)
        self.tasks = tasks.TasksResourceWithRawResponse(client.tasks)
        self.webhooks = webhooks.WebhooksResourceWithRawResponse(client.webhooks)


class AsyncIttybitWithRawResponse:
    def __init__(self, client: AsyncIttybit) -> None:
        self.automations = automations.AsyncAutomationsResourceWithRawResponse(client.automations)
        self.files = files.AsyncFilesResourceWithRawResponse(client.files)
        self.logs = logs.AsyncLogsResourceWithRawResponse(client.logs)
        self.events = events.AsyncEventsResourceWithRawResponse(client.events)
        self.media = media.AsyncMediaResourceWithRawResponse(client.media)
        self.projects = projects.AsyncProjectsResourceWithRawResponse(client.projects)
        self.tasks = tasks.AsyncTasksResourceWithRawResponse(client.tasks)
        self.webhooks = webhooks.AsyncWebhooksResourceWithRawResponse(client.webhooks)


class IttybitWithStreamedResponse:
    def __init__(self, client: Ittybit) -> None:
        self.automations = automations.AutomationsResourceWithStreamingResponse(client.automations)
        self.files = files.FilesResourceWithStreamingResponse(client.files)
        self.logs = logs.LogsResourceWithStreamingResponse(client.logs)
        self.events = events.EventsResourceWithStreamingResponse(client.events)
        self.media = media.MediaResourceWithStreamingResponse(client.media)
        self.projects = projects.ProjectsResourceWithStreamingResponse(client.projects)
        self.tasks = tasks.TasksResourceWithStreamingResponse(client.tasks)
        self.webhooks = webhooks.WebhooksResourceWithStreamingResponse(client.webhooks)


class AsyncIttybitWithStreamedResponse:
    def __init__(self, client: AsyncIttybit) -> None:
        self.automations = automations.AsyncAutomationsResourceWithStreamingResponse(client.automations)
        self.files = files.AsyncFilesResourceWithStreamingResponse(client.files)
        self.logs = logs.AsyncLogsResourceWithStreamingResponse(client.logs)
        self.events = events.AsyncEventsResourceWithStreamingResponse(client.events)
        self.media = media.AsyncMediaResourceWithStreamingResponse(client.media)
        self.projects = projects.AsyncProjectsResourceWithStreamingResponse(client.projects)
        self.tasks = tasks.AsyncTasksResourceWithStreamingResponse(client.tasks)
        self.webhooks = webhooks.AsyncWebhooksResourceWithStreamingResponse(client.webhooks)


Client = Ittybit

AsyncClient = AsyncIttybit
