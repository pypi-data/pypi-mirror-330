# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from ittybit import Ittybit, AsyncIttybit
from tests.utils import assert_matches_type
from ittybit.types import TaskConfigResponse, TaskCreateResponse, TaskRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTasks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Ittybit) -> None:
        task = client.tasks.create(
            kind="kind",
        )
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Ittybit) -> None:
        task = client.tasks.create(
            kind="kind",
            input={},
            url="url",
        )
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Ittybit) -> None:
        response = client.tasks.with_raw_response.create(
            kind="kind",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Ittybit) -> None:
        with client.tasks.with_streaming_response.create(
            kind="kind",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskCreateResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Ittybit) -> None:
        task = client.tasks.retrieve()
        assert_matches_type(TaskRetrieveResponse, task, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Ittybit) -> None:
        response = client.tasks.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskRetrieveResponse, task, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Ittybit) -> None:
        with client.tasks.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskRetrieveResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_config(self, client: Ittybit) -> None:
        task = client.tasks.config()
        assert_matches_type(TaskConfigResponse, task, path=["response"])

    @parametrize
    def test_raw_response_config(self, client: Ittybit) -> None:
        response = client.tasks.with_raw_response.config()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskConfigResponse, task, path=["response"])

    @parametrize
    def test_streaming_response_config(self, client: Ittybit) -> None:
        with client.tasks.with_streaming_response.config() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskConfigResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTasks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncIttybit) -> None:
        task = await async_client.tasks.create(
            kind="kind",
        )
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncIttybit) -> None:
        task = await async_client.tasks.create(
            kind="kind",
            input={},
            url="url",
        )
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncIttybit) -> None:
        response = await async_client.tasks.with_raw_response.create(
            kind="kind",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncIttybit) -> None:
        async with async_client.tasks.with_streaming_response.create(
            kind="kind",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskCreateResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncIttybit) -> None:
        task = await async_client.tasks.retrieve()
        assert_matches_type(TaskRetrieveResponse, task, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncIttybit) -> None:
        response = await async_client.tasks.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskRetrieveResponse, task, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncIttybit) -> None:
        async with async_client.tasks.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskRetrieveResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_config(self, async_client: AsyncIttybit) -> None:
        task = await async_client.tasks.config()
        assert_matches_type(TaskConfigResponse, task, path=["response"])

    @parametrize
    async def test_raw_response_config(self, async_client: AsyncIttybit) -> None:
        response = await async_client.tasks.with_raw_response.config()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskConfigResponse, task, path=["response"])

    @parametrize
    async def test_streaming_response_config(self, async_client: AsyncIttybit) -> None:
        async with async_client.tasks.with_streaming_response.config() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskConfigResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True
