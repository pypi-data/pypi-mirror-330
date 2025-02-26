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
from .resources import datasets, projects, evaluation, experiments, fine_tune_jobs, label_dataset_jobs
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import LastmileError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "Lastmile",
    "AsyncLastmile",
    "Client",
    "AsyncClient",
]


class Lastmile(SyncAPIClient):
    projects: projects.ProjectsResource
    experiments: experiments.ExperimentsResource
    datasets: datasets.DatasetsResource
    evaluation: evaluation.EvaluationResource
    fine_tune_jobs: fine_tune_jobs.FineTuneJobsResource
    label_dataset_jobs: label_dataset_jobs.LabelDatasetJobsResource
    with_raw_response: LastmileWithRawResponse
    with_streaming_response: LastmileWithStreamedResponse

    # client options
    bearer_token: str

    def __init__(
        self,
        *,
        bearer_token: str | None = None,
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
        """Construct a new synchronous lastmile client instance.

        This automatically infers the `bearer_token` argument from the `LASTMILE_API_TOKEN` environment variable if it is not provided.
        """
        if bearer_token is None:
            bearer_token = os.environ.get("LASTMILE_API_TOKEN")
        if bearer_token is None:
            raise LastmileError(
                "The bearer_token client option must be set either by passing bearer_token to the client or by setting the LASTMILE_API_TOKEN environment variable"
            )
        self.bearer_token = bearer_token

        if base_url is None:
            base_url = os.environ.get("LASTMILE_BASE_URL")
        if base_url is None:
            base_url = f"https://lastmileai.dev"

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

        self.projects = projects.ProjectsResource(self)
        self.experiments = experiments.ExperimentsResource(self)
        self.datasets = datasets.DatasetsResource(self)
        self.evaluation = evaluation.EvaluationResource(self)
        self.fine_tune_jobs = fine_tune_jobs.FineTuneJobsResource(self)
        self.label_dataset_jobs = label_dataset_jobs.LabelDatasetJobsResource(self)
        self.with_raw_response = LastmileWithRawResponse(self)
        self.with_streaming_response = LastmileWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        return {"Authorization": f"Bearer {bearer_token}"}

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
        bearer_token: str | None = None,
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
            bearer_token=bearer_token or self.bearer_token,
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


class AsyncLastmile(AsyncAPIClient):
    projects: projects.AsyncProjectsResource
    experiments: experiments.AsyncExperimentsResource
    datasets: datasets.AsyncDatasetsResource
    evaluation: evaluation.AsyncEvaluationResource
    fine_tune_jobs: fine_tune_jobs.AsyncFineTuneJobsResource
    label_dataset_jobs: label_dataset_jobs.AsyncLabelDatasetJobsResource
    with_raw_response: AsyncLastmileWithRawResponse
    with_streaming_response: AsyncLastmileWithStreamedResponse

    # client options
    bearer_token: str

    def __init__(
        self,
        *,
        bearer_token: str | None = None,
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
        """Construct a new async lastmile client instance.

        This automatically infers the `bearer_token` argument from the `LASTMILE_API_TOKEN` environment variable if it is not provided.
        """
        if bearer_token is None:
            bearer_token = os.environ.get("LASTMILE_API_TOKEN")
        if bearer_token is None:
            raise LastmileError(
                "The bearer_token client option must be set either by passing bearer_token to the client or by setting the LASTMILE_API_TOKEN environment variable"
            )
        self.bearer_token = bearer_token

        if base_url is None:
            base_url = os.environ.get("LASTMILE_BASE_URL")
        if base_url is None:
            base_url = f"https://lastmileai.dev"

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

        self.projects = projects.AsyncProjectsResource(self)
        self.experiments = experiments.AsyncExperimentsResource(self)
        self.datasets = datasets.AsyncDatasetsResource(self)
        self.evaluation = evaluation.AsyncEvaluationResource(self)
        self.fine_tune_jobs = fine_tune_jobs.AsyncFineTuneJobsResource(self)
        self.label_dataset_jobs = label_dataset_jobs.AsyncLabelDatasetJobsResource(self)
        self.with_raw_response = AsyncLastmileWithRawResponse(self)
        self.with_streaming_response = AsyncLastmileWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        return {"Authorization": f"Bearer {bearer_token}"}

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
        bearer_token: str | None = None,
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
            bearer_token=bearer_token or self.bearer_token,
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


class LastmileWithRawResponse:
    def __init__(self, client: Lastmile) -> None:
        self.projects = projects.ProjectsResourceWithRawResponse(client.projects)
        self.experiments = experiments.ExperimentsResourceWithRawResponse(client.experiments)
        self.datasets = datasets.DatasetsResourceWithRawResponse(client.datasets)
        self.evaluation = evaluation.EvaluationResourceWithRawResponse(client.evaluation)
        self.fine_tune_jobs = fine_tune_jobs.FineTuneJobsResourceWithRawResponse(client.fine_tune_jobs)
        self.label_dataset_jobs = label_dataset_jobs.LabelDatasetJobsResourceWithRawResponse(client.label_dataset_jobs)


class AsyncLastmileWithRawResponse:
    def __init__(self, client: AsyncLastmile) -> None:
        self.projects = projects.AsyncProjectsResourceWithRawResponse(client.projects)
        self.experiments = experiments.AsyncExperimentsResourceWithRawResponse(client.experiments)
        self.datasets = datasets.AsyncDatasetsResourceWithRawResponse(client.datasets)
        self.evaluation = evaluation.AsyncEvaluationResourceWithRawResponse(client.evaluation)
        self.fine_tune_jobs = fine_tune_jobs.AsyncFineTuneJobsResourceWithRawResponse(client.fine_tune_jobs)
        self.label_dataset_jobs = label_dataset_jobs.AsyncLabelDatasetJobsResourceWithRawResponse(
            client.label_dataset_jobs
        )


class LastmileWithStreamedResponse:
    def __init__(self, client: Lastmile) -> None:
        self.projects = projects.ProjectsResourceWithStreamingResponse(client.projects)
        self.experiments = experiments.ExperimentsResourceWithStreamingResponse(client.experiments)
        self.datasets = datasets.DatasetsResourceWithStreamingResponse(client.datasets)
        self.evaluation = evaluation.EvaluationResourceWithStreamingResponse(client.evaluation)
        self.fine_tune_jobs = fine_tune_jobs.FineTuneJobsResourceWithStreamingResponse(client.fine_tune_jobs)
        self.label_dataset_jobs = label_dataset_jobs.LabelDatasetJobsResourceWithStreamingResponse(
            client.label_dataset_jobs
        )


class AsyncLastmileWithStreamedResponse:
    def __init__(self, client: AsyncLastmile) -> None:
        self.projects = projects.AsyncProjectsResourceWithStreamingResponse(client.projects)
        self.experiments = experiments.AsyncExperimentsResourceWithStreamingResponse(client.experiments)
        self.datasets = datasets.AsyncDatasetsResourceWithStreamingResponse(client.datasets)
        self.evaluation = evaluation.AsyncEvaluationResourceWithStreamingResponse(client.evaluation)
        self.fine_tune_jobs = fine_tune_jobs.AsyncFineTuneJobsResourceWithStreamingResponse(client.fine_tune_jobs)
        self.label_dataset_jobs = label_dataset_jobs.AsyncLabelDatasetJobsResourceWithStreamingResponse(
            client.label_dataset_jobs
        )


Client = Lastmile

AsyncClient = AsyncLastmile
