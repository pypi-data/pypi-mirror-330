# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import assets_extract_extract_params, assets_extract_update_status_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.extract import Extract

__all__ = ["AssetsExtractResource", "AsyncAssetsExtractResource"]


class AssetsExtractResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AssetsExtractResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AssetsExtractResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AssetsExtractResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#with_streaming_response
        """
        return AssetsExtractResourceWithStreamingResponse(self)

    def extract(
        self,
        *,
        asset_ids: List[str] | NotGiven = NOT_GIVEN,
        blocking: bool | NotGiven = NOT_GIVEN,
        parse_strategy: Literal["optimized", "ocr", "xml", "markdown", "advanced_markdown"] | NotGiven = NOT_GIVEN,
        transform_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Extract:
        """
        A single unified endpoint that can:

        - Take in either `transform_id` or specific `asset_ids`.
        - Mark them for extraction (set status to PROCESSING, set parse strategy).
        - Kick off background extraction tasks.
        - If `blocking=true`, wait (up to 120s) for them to become PROCESSED, and return
          results.
        - If `blocking=false`, return immediately with the current statuses.

        The response returns an array of assets. If `blocking=true` and each asset
        finishes, the `data[i].status` will be PROCESSED and `extraction` will be
        fetched from your S3 store. Otherwise (non-blocking or timed out), the status
        might still be PROCESSING, and the `extraction` could be empty or not included.

        Args:
          asset_ids: Optional. Asset IDs to run extraction on. Overrides transform_id.

          blocking: Optional, defaults to False. If True, a response will come back after at most
              120 seconds with the extracted values.

          parse_strategy: Enum representing different parsing strategies. Note that OCR and XML will be
              deprecated soon.

          transform_id: Optional. Transformation ID of the transform housing the assets to extract.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/assets/extract",
            body=maybe_transform(
                {
                    "asset_ids": asset_ids,
                    "blocking": blocking,
                    "parse_strategy": parse_strategy,
                    "transform_id": transform_id,
                },
                assets_extract_extract_params.AssetsExtractExtractParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Extract,
        )

    def update_status(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Update Status

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._put(
            "/v1/assets/update_status",
            body=maybe_transform(body, assets_extract_update_status_params.AssetsExtractUpdateStatusParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncAssetsExtractResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAssetsExtractResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncAssetsExtractResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAssetsExtractResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#with_streaming_response
        """
        return AsyncAssetsExtractResourceWithStreamingResponse(self)

    async def extract(
        self,
        *,
        asset_ids: List[str] | NotGiven = NOT_GIVEN,
        blocking: bool | NotGiven = NOT_GIVEN,
        parse_strategy: Literal["optimized", "ocr", "xml", "markdown", "advanced_markdown"] | NotGiven = NOT_GIVEN,
        transform_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Extract:
        """
        A single unified endpoint that can:

        - Take in either `transform_id` or specific `asset_ids`.
        - Mark them for extraction (set status to PROCESSING, set parse strategy).
        - Kick off background extraction tasks.
        - If `blocking=true`, wait (up to 120s) for them to become PROCESSED, and return
          results.
        - If `blocking=false`, return immediately with the current statuses.

        The response returns an array of assets. If `blocking=true` and each asset
        finishes, the `data[i].status` will be PROCESSED and `extraction` will be
        fetched from your S3 store. Otherwise (non-blocking or timed out), the status
        might still be PROCESSING, and the `extraction` could be empty or not included.

        Args:
          asset_ids: Optional. Asset IDs to run extraction on. Overrides transform_id.

          blocking: Optional, defaults to False. If True, a response will come back after at most
              120 seconds with the extracted values.

          parse_strategy: Enum representing different parsing strategies. Note that OCR and XML will be
              deprecated soon.

          transform_id: Optional. Transformation ID of the transform housing the assets to extract.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/assets/extract",
            body=await async_maybe_transform(
                {
                    "asset_ids": asset_ids,
                    "blocking": blocking,
                    "parse_strategy": parse_strategy,
                    "transform_id": transform_id,
                },
                assets_extract_extract_params.AssetsExtractExtractParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Extract,
        )

    async def update_status(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Update Status

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            "/v1/assets/update_status",
            body=await async_maybe_transform(body, assets_extract_update_status_params.AssetsExtractUpdateStatusParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AssetsExtractResourceWithRawResponse:
    def __init__(self, assets_extract: AssetsExtractResource) -> None:
        self._assets_extract = assets_extract

        self.extract = to_raw_response_wrapper(
            assets_extract.extract,
        )
        self.update_status = to_raw_response_wrapper(
            assets_extract.update_status,
        )


class AsyncAssetsExtractResourceWithRawResponse:
    def __init__(self, assets_extract: AsyncAssetsExtractResource) -> None:
        self._assets_extract = assets_extract

        self.extract = async_to_raw_response_wrapper(
            assets_extract.extract,
        )
        self.update_status = async_to_raw_response_wrapper(
            assets_extract.update_status,
        )


class AssetsExtractResourceWithStreamingResponse:
    def __init__(self, assets_extract: AssetsExtractResource) -> None:
        self._assets_extract = assets_extract

        self.extract = to_streamed_response_wrapper(
            assets_extract.extract,
        )
        self.update_status = to_streamed_response_wrapper(
            assets_extract.update_status,
        )


class AsyncAssetsExtractResourceWithStreamingResponse:
    def __init__(self, assets_extract: AsyncAssetsExtractResource) -> None:
        self._assets_extract = assets_extract

        self.extract = async_to_streamed_response_wrapper(
            assets_extract.extract,
        )
        self.update_status = async_to_streamed_response_wrapper(
            assets_extract.update_status,
        )
