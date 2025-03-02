# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from ittybit import Ittybit, AsyncIttybit
from tests.utils import assert_matches_type
from ittybit.types import EventListResponse, EventRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Ittybit) -> None:
        event = client.events.retrieve()
        assert_matches_type(EventRetrieveResponse, event, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Ittybit) -> None:
        response = client.events.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(EventRetrieveResponse, event, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Ittybit) -> None:
        with client.events.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(EventRetrieveResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: Ittybit) -> None:
        event = client.events.list()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Ittybit) -> None:
        response = client.events.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Ittybit) -> None:
        with client.events.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(EventListResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEvents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncIttybit) -> None:
        event = await async_client.events.retrieve()
        assert_matches_type(EventRetrieveResponse, event, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncIttybit) -> None:
        response = await async_client.events.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(EventRetrieveResponse, event, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncIttybit) -> None:
        async with async_client.events.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(EventRetrieveResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncIttybit) -> None:
        event = await async_client.events.list()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncIttybit) -> None:
        response = await async_client.events.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(EventListResponse, event, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncIttybit) -> None:
        async with async_client.events.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(EventListResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True
