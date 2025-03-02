# noqa: I001
from __future__ import annotations

import os
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
        filename: str,
        size: int,
        folder: str | NotGiven = NOT_GIVEN,
        label: str | NotGiven = NOT_GIVEN,
        alt: str | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        metadata: dict | NotGiven = NOT_GIVEN,
        timeout: int | NotGiven = NOT_GIVEN,
        async_upload: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        request_timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileCreateResponse:
        """
        Create an upload session and get the upload URL.

        Args:
            filename: File name with extension
            size: Size of the file to be uploaded in bytes
            folder: Folder path (optional)
            label: Label for the file
            alt: Alt text for the file
            title: Title for the file
            metadata: Additional metadata for the file
            timeout: Upload timeout in seconds
            async_upload: Whether to process the upload asynchronously
            extra_headers: Send extra headers
            extra_query: Add additional query parameters to the request
            extra_body: Add additional JSON properties to the request
            request_timeout: Override the client-level default timeout for this request, in seconds
        """
        body = {
            "filename": filename,
            "size": size,
        }

        if folder is not NOT_GIVEN:
            body["folder"] = folder
        if label is not NOT_GIVEN:
            body["label"] = label
        if alt is not NOT_GIVEN:
            body["alt"] = alt
        if title is not NOT_GIVEN:
            body["title"] = title
        if metadata is not NOT_GIVEN:
            body["metadata"] = metadata
        if timeout is not NOT_GIVEN:
            body["timeout"] = timeout
        if async_upload is not NOT_GIVEN:
            body["async"] = async_upload

        return self._post(
            "/uploads",
            body=body,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=request_timeout
            ),
            cast_to=FileCreateResponse,
        )

    def upload(
        self,
        file: BinaryIO,
        filename: str,
        *,
        folder: str | NotGiven = NOT_GIVEN,
        label: str | NotGiven = NOT_GIVEN,
        alt: str | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        metadata: dict | NotGiven = NOT_GIVEN,
        timeout: int | NotGiven = NOT_GIVEN,
        async_upload: bool | NotGiven = NOT_GIVEN,
        content_type: str | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        request_timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileCreateResponse:
        """
        Upload a file by first creating a session then uploading to the provided URL.

        Args:
            file: A file-like object to upload
            filename: File name with extension
            folder: Folder path (optional)
            label: Label for the file
            alt: Alt text for the file
            title: Title for the file
            metadata: Additional metadata for the file
            timeout: Upload timeout in seconds
            async_upload: Whether to process the upload asynchronously
            content_type: Optional MIME type of the file
            extra_headers: Send extra headers
            extra_query: Add additional query parameters to the request
            extra_body: Add additional JSON properties to the request
            request_timeout: Override the client-level default timeout for this request, in seconds
        """
        file_size = self._get_file_size(file)
        session_response = self.create_upload_session(
            filename=filename,
            size=file_size,
            folder=folder,
            label=label,
            alt=alt,
            title=title,
            metadata=metadata,
            timeout=timeout,
            async_upload=async_upload,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            request_timeout=request_timeout
        )
        data = session_response.model_dump()
        upload_url = data["url"]
        
        headers = {}
        if content_type is not NOT_GIVEN:
            headers['Content-Type'] = content_type

        if file_size <= 5 * 1024 * 1024:  # 5MB
            return self._upload_single(
                file,
                upload_url,
                headers,
                timeout=request_timeout
            )
        else:
            return self._upload_chunked(
                file,
                file_size,
                upload_url,
                headers,
                timeout=request_timeout
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
        headers: dict[str, str],
        *,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileCreateResponse:
        """Handle single-part upload for files <= 5MB."""
        response = self._put(
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
        headers: dict[str, str],
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
            
            response = self._put(
                upload_url,
                content=chunk_data,
                headers=chunk_headers,
                timeout=timeout
            )
            
            # Return the response from the final chunk
            if chunk_number == total_chunks - 1:
                return FileCreateResponse(response)
            
            response.raise_for_status()
            
        raise RuntimeError("Upload failed - no chunks were processed")


class AsyncUploaderResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUploaderResourceWithRawResponse:
        return AsyncUploaderResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUploaderResourceWithStreamingResponse:
        return AsyncUploaderResourceWithStreamingResponse(self)

    async def create_upload_session(
        self,
        *,
        filename: str,
        size: int,
        folder: str | NotGiven = NOT_GIVEN,
        label: str | NotGiven = NOT_GIVEN,
        alt: str | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        metadata: dict | NotGiven = NOT_GIVEN,
        timeout: int | NotGiven = NOT_GIVEN,
        async_upload: bool | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        request_timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileCreateResponse:
        body = {
            "filename": filename,
            "size": size,
        }

        if folder is not NOT_GIVEN:
            body["folder"] = folder
        if label is not NOT_GIVEN:
            body["label"] = label
        if alt is not NOT_GIVEN:
            body["alt"] = alt
        if title is not NOT_GIVEN:
            body["title"] = title
        if metadata is not NOT_GIVEN:
            body["metadata"] = metadata
        if timeout is not NOT_GIVEN:
            body["timeout"] = timeout
        if async_upload is not NOT_GIVEN:
            body["async"] = async_upload

        return await self._post(
            "/files/upload-session",
            body=body,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=request_timeout
            ),
            cast_to=FileCreateResponse,
        )

    async def upload(
        self,
        file: BinaryIO,
        filename: str,
        *,
        folder: str | NotGiven = NOT_GIVEN,
        label: str | NotGiven = NOT_GIVEN,
        alt: str | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        metadata: dict | NotGiven = NOT_GIVEN,
        timeout: int | NotGiven = NOT_GIVEN,
        async_upload: bool | NotGiven = NOT_GIVEN,
        content_type: str | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        request_timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileCreateResponse:
        file_size = UploaderResource._get_file_size(file)
        session_response = await self.create_upload_session(
            filename=filename,
            size=file_size,
            folder=folder,
            label=label,
            alt=alt,
            title=title,
            metadata=metadata,
            timeout=timeout,
            async_upload=async_upload,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            request_timeout=request_timeout
        )
        data = session_response.model_dump()
        upload_url = data["url"]
        
        headers = {}
        if content_type is not NOT_GIVEN:
            headers['Content-Type'] = content_type

        if file_size <= 5 * 1024 * 1024:  # 5MB
            return await self._upload_single(
                file,
                upload_url,
                headers,
                timeout=request_timeout
            )
        else:
            return await self._upload_chunked(
                file,
                file_size,
                upload_url,
                headers,
                timeout=request_timeout
            )

    async def _upload_single(
        self,
        file: BinaryIO,
        upload_url: str,
        headers: dict[str, str],
        *,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileCreateResponse:
        response = await self._put(
            upload_url,
            content=file,
            headers=headers,
            timeout=timeout
        )
        return FileCreateResponse(response)

    async def _upload_chunked(
        self,
        file: BinaryIO,
        file_size: int,
        upload_url: str,
        headers: dict[str, str],
        *,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileCreateResponse:
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
            
            response = await self._put(
                upload_url,
                content=chunk_data,
                headers=chunk_headers,
                timeout=timeout
            )
            
            if chunk_number == total_chunks - 1:
                return FileCreateResponse(response)
            
            response.raise_for_status()
            
        raise RuntimeError("Upload failed - no chunks were processed")


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
