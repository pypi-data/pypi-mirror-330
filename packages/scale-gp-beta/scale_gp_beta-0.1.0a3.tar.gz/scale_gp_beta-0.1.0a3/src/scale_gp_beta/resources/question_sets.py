# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, overload

import httpx

from ..types import (
    question_set_list_params,
    question_set_create_params,
    question_set_update_params,
    question_set_retrieve_params,
)
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
from ..pagination import SyncCursorPage, AsyncCursorPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.question_set import QuestionSet
from ..types.question_set_delete_response import QuestionSetDeleteResponse

__all__ = ["QuestionSetsResource", "AsyncQuestionSetsResource"]


class QuestionSetsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> QuestionSetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return QuestionSetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> QuestionSetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return QuestionSetsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        questions: List[question_set_create_params.Question],
        instructions: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuestionSet:
        """
        Create Question Set

        Args:
          questions: IDs of existing questions in the question set or new questions to create. You
              can also optionally specify configurations for each question. Example:
              [`question_id`, {'id': 'question_id2', 'configuration': {...}}, {'title': 'New
              question', ...}]

          instructions: Instructions to answer questions

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/question-sets",
            body=maybe_transform(
                {
                    "name": name,
                    "questions": questions,
                    "instructions": instructions,
                },
                question_set_create_params.QuestionSetCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QuestionSet,
        )

    def retrieve(
        self,
        question_set_id: str,
        *,
        views: List[Literal["questions"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuestionSet:
        """
        Get Question Set

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_set_id:
            raise ValueError(f"Expected a non-empty value for `question_set_id` but received {question_set_id!r}")
        return self._get(
            f"/v5/question-sets/{question_set_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"views": views}, question_set_retrieve_params.QuestionSetRetrieveParams),
            ),
            cast_to=QuestionSet,
        )

    @overload
    def update(
        self,
        question_set_id: str,
        *,
        instructions: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuestionSet:
        """
        Update Question Set

        Args:
          instructions: Instructions to answer questions

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def update(
        self,
        question_set_id: str,
        *,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuestionSet:
        """
        Update Question Set

        Args:
          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    def update(
        self,
        question_set_id: str,
        *,
        instructions: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        restore: Literal[True] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuestionSet:
        if not question_set_id:
            raise ValueError(f"Expected a non-empty value for `question_set_id` but received {question_set_id!r}")
        return self._patch(
            f"/v5/question-sets/{question_set_id}",
            body=maybe_transform(
                {
                    "instructions": instructions,
                    "name": name,
                    "restore": restore,
                },
                question_set_update_params.QuestionSetUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QuestionSet,
        )

    def list(
        self,
        *,
        ending_before: Optional[str] | NotGiven = NOT_GIVEN,
        include_archived: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: Optional[str] | NotGiven = NOT_GIVEN,
        views: List[Literal["questions"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[QuestionSet]:
        """
        List Question Sets

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/question-sets",
            page=SyncCursorPage[QuestionSet],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "include_archived": include_archived,
                        "limit": limit,
                        "starting_after": starting_after,
                        "views": views,
                    },
                    question_set_list_params.QuestionSetListParams,
                ),
            ),
            model=QuestionSet,
        )

    def delete(
        self,
        question_set_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuestionSetDeleteResponse:
        """
        Archive Question Set

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_set_id:
            raise ValueError(f"Expected a non-empty value for `question_set_id` but received {question_set_id!r}")
        return self._delete(
            f"/v5/question-sets/{question_set_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QuestionSetDeleteResponse,
        )


class AsyncQuestionSetsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncQuestionSetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncQuestionSetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncQuestionSetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncQuestionSetsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        questions: List[question_set_create_params.Question],
        instructions: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuestionSet:
        """
        Create Question Set

        Args:
          questions: IDs of existing questions in the question set or new questions to create. You
              can also optionally specify configurations for each question. Example:
              [`question_id`, {'id': 'question_id2', 'configuration': {...}}, {'title': 'New
              question', ...}]

          instructions: Instructions to answer questions

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/question-sets",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "questions": questions,
                    "instructions": instructions,
                },
                question_set_create_params.QuestionSetCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QuestionSet,
        )

    async def retrieve(
        self,
        question_set_id: str,
        *,
        views: List[Literal["questions"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuestionSet:
        """
        Get Question Set

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_set_id:
            raise ValueError(f"Expected a non-empty value for `question_set_id` but received {question_set_id!r}")
        return await self._get(
            f"/v5/question-sets/{question_set_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"views": views}, question_set_retrieve_params.QuestionSetRetrieveParams
                ),
            ),
            cast_to=QuestionSet,
        )

    @overload
    async def update(
        self,
        question_set_id: str,
        *,
        instructions: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuestionSet:
        """
        Update Question Set

        Args:
          instructions: Instructions to answer questions

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def update(
        self,
        question_set_id: str,
        *,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuestionSet:
        """
        Update Question Set

        Args:
          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    async def update(
        self,
        question_set_id: str,
        *,
        instructions: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        restore: Literal[True] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuestionSet:
        if not question_set_id:
            raise ValueError(f"Expected a non-empty value for `question_set_id` but received {question_set_id!r}")
        return await self._patch(
            f"/v5/question-sets/{question_set_id}",
            body=await async_maybe_transform(
                {
                    "instructions": instructions,
                    "name": name,
                    "restore": restore,
                },
                question_set_update_params.QuestionSetUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QuestionSet,
        )

    def list(
        self,
        *,
        ending_before: Optional[str] | NotGiven = NOT_GIVEN,
        include_archived: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: Optional[str] | NotGiven = NOT_GIVEN,
        views: List[Literal["questions"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[QuestionSet, AsyncCursorPage[QuestionSet]]:
        """
        List Question Sets

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/question-sets",
            page=AsyncCursorPage[QuestionSet],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "include_archived": include_archived,
                        "limit": limit,
                        "starting_after": starting_after,
                        "views": views,
                    },
                    question_set_list_params.QuestionSetListParams,
                ),
            ),
            model=QuestionSet,
        )

    async def delete(
        self,
        question_set_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> QuestionSetDeleteResponse:
        """
        Archive Question Set

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_set_id:
            raise ValueError(f"Expected a non-empty value for `question_set_id` but received {question_set_id!r}")
        return await self._delete(
            f"/v5/question-sets/{question_set_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QuestionSetDeleteResponse,
        )


class QuestionSetsResourceWithRawResponse:
    def __init__(self, question_sets: QuestionSetsResource) -> None:
        self._question_sets = question_sets

        self.create = to_raw_response_wrapper(
            question_sets.create,
        )
        self.retrieve = to_raw_response_wrapper(
            question_sets.retrieve,
        )
        self.update = to_raw_response_wrapper(
            question_sets.update,
        )
        self.list = to_raw_response_wrapper(
            question_sets.list,
        )
        self.delete = to_raw_response_wrapper(
            question_sets.delete,
        )


class AsyncQuestionSetsResourceWithRawResponse:
    def __init__(self, question_sets: AsyncQuestionSetsResource) -> None:
        self._question_sets = question_sets

        self.create = async_to_raw_response_wrapper(
            question_sets.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            question_sets.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            question_sets.update,
        )
        self.list = async_to_raw_response_wrapper(
            question_sets.list,
        )
        self.delete = async_to_raw_response_wrapper(
            question_sets.delete,
        )


class QuestionSetsResourceWithStreamingResponse:
    def __init__(self, question_sets: QuestionSetsResource) -> None:
        self._question_sets = question_sets

        self.create = to_streamed_response_wrapper(
            question_sets.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            question_sets.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            question_sets.update,
        )
        self.list = to_streamed_response_wrapper(
            question_sets.list,
        )
        self.delete = to_streamed_response_wrapper(
            question_sets.delete,
        )


class AsyncQuestionSetsResourceWithStreamingResponse:
    def __init__(self, question_sets: AsyncQuestionSetsResource) -> None:
        self._question_sets = question_sets

        self.create = async_to_streamed_response_wrapper(
            question_sets.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            question_sets.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            question_sets.update,
        )
        self.list = async_to_streamed_response_wrapper(
            question_sets.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            question_sets.delete,
        )
