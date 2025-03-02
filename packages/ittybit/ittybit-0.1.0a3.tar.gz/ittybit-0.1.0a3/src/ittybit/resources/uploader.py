# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import BinaryIO

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.file_create_response import FileCreateResponse

__all__ = ["UploaderResource", "AsyncUploaderResource"]


class UploaderResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UploaderResourceWithRawResponse:
        return UploaderResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UploaderResourceWithStreamingResponse:
        return UploaderResourceWithStreamingResponse(self)

    def create_upload_session(
        self,
        *,
        path: str,
        size: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileCreateResponse:
        """
        Create an upload session and get the upload URL.

        Args:
            path: The path where the file should be uploaded
            size: Size of the file to be uploaded in bytes
            extra_headers: Send extra headers
            extra_query: Add additional query parameters to the request
            extra_body: Add additional JSON properties to the request
            timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/files/upload-session",
            body={
                "path": path,
                "size": size
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout
            ),
            cast_to=FileCreateResponse,
        )

    def upload(
        self,
        file: BinaryIO,
        path: str,
        *,
        content_type: str | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileCreateResponse:
        """
        Upload a file by first creating a session then uploading to the provided URL.

        Args:
            file: A file-like object to upload
            path: The path where the file should be uploaded
            content_type: Optional MIME type of the file
            extra_headers: Send extra headers
            extra_query: Add additional query parameters to the request
            extra_body: Add additional JSON properties to the request
            timeout: Override the client-level default timeout for this request, in seconds
        """
        file_size = self._get_file_size(file)
        session_response = self.create_upload_session(
            path=path,
            size=file_size,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout
        )
        upload_url = session_response.json()["url"]
        
        headers = {}
        if content_type is not NOT_GIVEN:
            headers['Content-Type'] = content_type

        if file_size <= 5 * 1024 * 1024:  # 5MB
            return self._upload_single(
                file,
                upload_url,
                headers,
                timeout=timeout
            )
        else:
            return self._upload_chunked(
                file,
                file_size,
                upload_url,
                headers,
                timeout=timeout
            )

    @staticmethod
    def _get_file_size(file: BinaryIO) -> int:
        """Get the size of a file-like object."""
        current_pos = file.tell()
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(current_pos)
        return size

    def _upload_single(
        self,
        file: BinaryIO,
        upload_url: str,
        headers: dict,
        *,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileCreateResponse:
        """Handle single-part upload for files <= 5MB."""
        response = self.client.put(
            upload_url,
            content=file,
            headers=headers,
            timeout=timeout
        )
        return FileCreateResponse(response)

    def _upload_chunked(
        self,
        file: BinaryIO,
        file_size: int,
        upload_url: str,
        headers: dict,
        *,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileCreateResponse:
        """Handle chunked upload for files > 5MB."""
        chunk_size = 5 * 1024 * 1024  # 5MB
        total_chunks = (file_size + chunk_size - 1) // chunk_size
        
        for chunk_number in range(total_chunks):
            start_byte = chunk_number * chunk_size
            end_byte = min(start_byte + chunk_size, file_size)
            content_length = end_byte - start_byte

            chunk_headers = {
                **headers,
                'Content-Range': f'bytes {start_byte}-{end_byte-1}/{file_size}',
                'Content-Length': str(content_length)
            }

            chunk_data = file.read(chunk_size)
            
            response = self.client.put(
                upload_url,
                content=chunk_data,
                headers=chunk_headers,
                timeout=timeout
            )
            
            # Return the response from the final chunk
            if chunk_number == total_chunks - 1:
                return FileCreateResponse(response)
            
            response.raise_for_status()


class AsyncUploaderResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUploaderResourceWithRawResponse:
        return AsyncUploaderResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUploaderResourceWithStreamingResponse:
        return AsyncUploaderResourceWithStreamingResponse(self)

    # Add async versions of the methods here...
    # (I can provide the async implementations if needed)


class UploaderResourceWithRawResponse:
    def __init__(self, uploader: UploaderResource) -> None:
        self._uploader = uploader

        self.create_upload_session = to_raw_response_wrapper(
            uploader.create_upload_session,
        )
        self.upload = to_raw_response_wrapper(
            uploader.upload,
        )


class AsyncUploaderResourceWithRawResponse:
    def __init__(self, uploader: AsyncUploaderResource) -> None:
        self._uploader = uploader

        self.create_upload_session = async_to_raw_response_wrapper(
            uploader.create_upload_session,
        )
        self.upload = async_to_raw_response_wrapper(
            uploader.upload,
        )


class UploaderResourceWithStreamingResponse:
    def __init__(self, uploader: UploaderResource) -> None:
        self._uploader = uploader

        self.create_upload_session = to_streamed_response_wrapper(
            uploader.create_upload_session,
        )
        self.upload = to_streamed_response_wrapper(
            uploader.upload,
        )


class AsyncUploaderResourceWithStreamingResponse:
    def __init__(self, uploader: AsyncUploaderResource) -> None:
        self._uploader = uploader

        self.create_upload_session = async_to_streamed_response_wrapper(
            uploader.create_upload_session,
        )
        self.upload = async_to_streamed_response_wrapper(
            uploader.upload,
        ) 