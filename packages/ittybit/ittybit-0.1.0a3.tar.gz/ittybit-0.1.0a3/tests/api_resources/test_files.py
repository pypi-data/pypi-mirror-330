# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from ittybit import Ittybit, AsyncIttybit
from tests.utils import assert_matches_type
from ittybit.types import (
    FileListResponse,
    FileCreateResponse,
    FileUploadResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Ittybit) -> None:
        file = client.files.create(
            filename="filename",
        )
        assert_matches_type(FileCreateResponse, file, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Ittybit) -> None:
        file = client.files.create(
            filename="filename",
            folder="folder",
            kind="video",
        )
        assert_matches_type(FileCreateResponse, file, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Ittybit) -> None:
        response = client.files.with_raw_response.create(
            filename="filename",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FileCreateResponse, file, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Ittybit) -> None:
        with client.files.with_streaming_response.create(
            filename="filename",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(FileCreateResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Ittybit) -> None:
        file = client.files.retrieve(
            "id",
        )
        assert file is None

    @parametrize
    def test_raw_response_retrieve(self, client: Ittybit) -> None:
        response = client.files.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert file is None

    @parametrize
    def test_streaming_response_retrieve(self, client: Ittybit) -> None:
        with client.files.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert file is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Ittybit) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.files.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Ittybit) -> None:
        file = client.files.update(
            id="id",
        )
        assert file is None

    @parametrize
    def test_method_update_with_all_params(self, client: Ittybit) -> None:
        file = client.files.update(
            id="id",
            content="content",
        )
        assert file is None

    @parametrize
    def test_raw_response_update(self, client: Ittybit) -> None:
        response = client.files.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert file is None

    @parametrize
    def test_streaming_response_update(self, client: Ittybit) -> None:
        with client.files.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert file is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Ittybit) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.files.with_raw_response.update(
                id="",
            )

    @parametrize
    def test_method_list(self, client: Ittybit) -> None:
        file = client.files.list()
        assert_matches_type(FileListResponse, file, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Ittybit) -> None:
        file = client.files.list(
            limit=1,
            page=1,
        )
        assert_matches_type(FileListResponse, file, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Ittybit) -> None:
        response = client.files.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FileListResponse, file, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Ittybit) -> None:
        with client.files.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(FileListResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Ittybit) -> None:
        file = client.files.delete(
            "id",
        )
        assert file is None

    @parametrize
    def test_raw_response_delete(self, client: Ittybit) -> None:
        response = client.files.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert file is None

    @parametrize
    def test_streaming_response_delete(self, client: Ittybit) -> None:
        with client.files.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert file is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Ittybit) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.files.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_upload(self, client: Ittybit) -> None:
        file = client.files.upload()
        assert_matches_type(FileUploadResponse, file, path=["response"])

    @parametrize
    def test_method_upload_with_all_params(self, client: Ittybit) -> None:
        file = client.files.upload(
            chunk_number=0,
            chunk_size=0,
            content="content",
            total_chunks=0,
        )
        assert_matches_type(FileUploadResponse, file, path=["response"])

    @parametrize
    def test_raw_response_upload(self, client: Ittybit) -> None:
        response = client.files.with_raw_response.upload()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FileUploadResponse, file, path=["response"])

    @parametrize
    def test_streaming_response_upload(self, client: Ittybit) -> None:
        with client.files.with_streaming_response.upload() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(FileUploadResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncFiles:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncIttybit) -> None:
        file = await async_client.files.create(
            filename="filename",
        )
        assert_matches_type(FileCreateResponse, file, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncIttybit) -> None:
        file = await async_client.files.create(
            filename="filename",
            folder="folder",
            kind="video",
        )
        assert_matches_type(FileCreateResponse, file, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncIttybit) -> None:
        response = await async_client.files.with_raw_response.create(
            filename="filename",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert_matches_type(FileCreateResponse, file, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncIttybit) -> None:
        async with async_client.files.with_streaming_response.create(
            filename="filename",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(FileCreateResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncIttybit) -> None:
        file = await async_client.files.retrieve(
            "id",
        )
        assert file is None

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncIttybit) -> None:
        response = await async_client.files.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert file is None

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncIttybit) -> None:
        async with async_client.files.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert file is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncIttybit) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.files.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncIttybit) -> None:
        file = await async_client.files.update(
            id="id",
        )
        assert file is None

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncIttybit) -> None:
        file = await async_client.files.update(
            id="id",
            content="content",
        )
        assert file is None

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncIttybit) -> None:
        response = await async_client.files.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert file is None

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncIttybit) -> None:
        async with async_client.files.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert file is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncIttybit) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.files.with_raw_response.update(
                id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncIttybit) -> None:
        file = await async_client.files.list()
        assert_matches_type(FileListResponse, file, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncIttybit) -> None:
        file = await async_client.files.list(
            limit=1,
            page=1,
        )
        assert_matches_type(FileListResponse, file, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncIttybit) -> None:
        response = await async_client.files.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert_matches_type(FileListResponse, file, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncIttybit) -> None:
        async with async_client.files.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(FileListResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncIttybit) -> None:
        file = await async_client.files.delete(
            "id",
        )
        assert file is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncIttybit) -> None:
        response = await async_client.files.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert file is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncIttybit) -> None:
        async with async_client.files.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert file is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncIttybit) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.files.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_upload(self, async_client: AsyncIttybit) -> None:
        file = await async_client.files.upload()
        assert_matches_type(FileUploadResponse, file, path=["response"])

    @parametrize
    async def test_method_upload_with_all_params(self, async_client: AsyncIttybit) -> None:
        file = await async_client.files.upload(
            chunk_number=0,
            chunk_size=0,
            content="content",
            total_chunks=0,
        )
        assert_matches_type(FileUploadResponse, file, path=["response"])

    @parametrize
    async def test_raw_response_upload(self, async_client: AsyncIttybit) -> None:
        response = await async_client.files.with_raw_response.upload()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert_matches_type(FileUploadResponse, file, path=["response"])

    @parametrize
    async def test_streaming_response_upload(self, async_client: AsyncIttybit) -> None:
        async with async_client.files.with_streaming_response.upload() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(FileUploadResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True
