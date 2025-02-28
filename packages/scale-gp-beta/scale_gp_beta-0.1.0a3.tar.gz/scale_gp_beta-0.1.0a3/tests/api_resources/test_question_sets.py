# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import (
    QuestionSet,
    QuestionSetDeleteResponse,
)
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestQuestionSets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        question_set = client.question_sets.create(
            name="name",
            questions=[
                {
                    "prompt": "prompt",
                    "title": "title",
                    "type": "categorical",
                }
            ],
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        question_set = client.question_sets.create(
            name="name",
            questions=[
                {
                    "prompt": "prompt",
                    "title": "title",
                    "type": "categorical",
                    "choices": [
                        {
                            "label": "label",
                            "value": "string",
                            "audit_required": True,
                        }
                    ],
                    "conditions": [{"foo": "bar"}],
                    "dropdown": True,
                    "multi": True,
                    "number_options": {
                        "max": 0,
                        "min": 0,
                    },
                    "override_config": {"required": True},
                    "rating_options": {
                        "max_label": "maxLabel",
                        "min_label": "minLabel",
                        "scale_steps": 0,
                    },
                    "required": True,
                }
            ],
            instructions="instructions",
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.question_sets.with_raw_response.create(
            name="name",
            questions=[
                {
                    "prompt": "prompt",
                    "title": "title",
                    "type": "categorical",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question_set = response.parse()
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.question_sets.with_streaming_response.create(
            name="name",
            questions=[
                {
                    "prompt": "prompt",
                    "title": "title",
                    "type": "categorical",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question_set = response.parse()
            assert_matches_type(QuestionSet, question_set, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        question_set = client.question_sets.retrieve(
            question_set_id="question_set_id",
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: SGPClient) -> None:
        question_set = client.question_sets.retrieve(
            question_set_id="question_set_id",
            views=["questions"],
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.question_sets.with_raw_response.retrieve(
            question_set_id="question_set_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question_set = response.parse()
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.question_sets.with_streaming_response.retrieve(
            question_set_id="question_set_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question_set = response.parse()
            assert_matches_type(QuestionSet, question_set, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_set_id` but received ''"):
            client.question_sets.with_raw_response.retrieve(
                question_set_id="",
            )

    @parametrize
    def test_method_update_overload_1(self, client: SGPClient) -> None:
        question_set = client.question_sets.update(
            question_set_id="question_set_id",
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    def test_method_update_with_all_params_overload_1(self, client: SGPClient) -> None:
        question_set = client.question_sets.update(
            question_set_id="question_set_id",
            instructions="instructions",
            name="name",
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    def test_raw_response_update_overload_1(self, client: SGPClient) -> None:
        response = client.question_sets.with_raw_response.update(
            question_set_id="question_set_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question_set = response.parse()
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    def test_streaming_response_update_overload_1(self, client: SGPClient) -> None:
        with client.question_sets.with_streaming_response.update(
            question_set_id="question_set_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question_set = response.parse()
            assert_matches_type(QuestionSet, question_set, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_overload_1(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_set_id` but received ''"):
            client.question_sets.with_raw_response.update(
                question_set_id="",
            )

    @parametrize
    def test_method_update_overload_2(self, client: SGPClient) -> None:
        question_set = client.question_sets.update(
            question_set_id="question_set_id",
            restore=True,
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    def test_raw_response_update_overload_2(self, client: SGPClient) -> None:
        response = client.question_sets.with_raw_response.update(
            question_set_id="question_set_id",
            restore=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question_set = response.parse()
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    def test_streaming_response_update_overload_2(self, client: SGPClient) -> None:
        with client.question_sets.with_streaming_response.update(
            question_set_id="question_set_id",
            restore=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question_set = response.parse()
            assert_matches_type(QuestionSet, question_set, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_overload_2(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_set_id` but received ''"):
            client.question_sets.with_raw_response.update(
                question_set_id="",
                restore=True,
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        question_set = client.question_sets.list()
        assert_matches_type(SyncCursorPage[QuestionSet], question_set, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        question_set = client.question_sets.list(
            ending_before="ending_before",
            include_archived=True,
            limit=1,
            starting_after="starting_after",
            views=["questions"],
        )
        assert_matches_type(SyncCursorPage[QuestionSet], question_set, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.question_sets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question_set = response.parse()
        assert_matches_type(SyncCursorPage[QuestionSet], question_set, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.question_sets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question_set = response.parse()
            assert_matches_type(SyncCursorPage[QuestionSet], question_set, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SGPClient) -> None:
        question_set = client.question_sets.delete(
            "question_set_id",
        )
        assert_matches_type(QuestionSetDeleteResponse, question_set, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SGPClient) -> None:
        response = client.question_sets.with_raw_response.delete(
            "question_set_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question_set = response.parse()
        assert_matches_type(QuestionSetDeleteResponse, question_set, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SGPClient) -> None:
        with client.question_sets.with_streaming_response.delete(
            "question_set_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question_set = response.parse()
            assert_matches_type(QuestionSetDeleteResponse, question_set, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_set_id` but received ''"):
            client.question_sets.with_raw_response.delete(
                "",
            )


class TestAsyncQuestionSets:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        question_set = await async_client.question_sets.create(
            name="name",
            questions=[
                {
                    "prompt": "prompt",
                    "title": "title",
                    "type": "categorical",
                }
            ],
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        question_set = await async_client.question_sets.create(
            name="name",
            questions=[
                {
                    "prompt": "prompt",
                    "title": "title",
                    "type": "categorical",
                    "choices": [
                        {
                            "label": "label",
                            "value": "string",
                            "audit_required": True,
                        }
                    ],
                    "conditions": [{"foo": "bar"}],
                    "dropdown": True,
                    "multi": True,
                    "number_options": {
                        "max": 0,
                        "min": 0,
                    },
                    "override_config": {"required": True},
                    "rating_options": {
                        "max_label": "maxLabel",
                        "min_label": "minLabel",
                        "scale_steps": 0,
                    },
                    "required": True,
                }
            ],
            instructions="instructions",
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.question_sets.with_raw_response.create(
            name="name",
            questions=[
                {
                    "prompt": "prompt",
                    "title": "title",
                    "type": "categorical",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question_set = await response.parse()
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.question_sets.with_streaming_response.create(
            name="name",
            questions=[
                {
                    "prompt": "prompt",
                    "title": "title",
                    "type": "categorical",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question_set = await response.parse()
            assert_matches_type(QuestionSet, question_set, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        question_set = await async_client.question_sets.retrieve(
            question_set_id="question_set_id",
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncSGPClient) -> None:
        question_set = await async_client.question_sets.retrieve(
            question_set_id="question_set_id",
            views=["questions"],
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.question_sets.with_raw_response.retrieve(
            question_set_id="question_set_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question_set = await response.parse()
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.question_sets.with_streaming_response.retrieve(
            question_set_id="question_set_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question_set = await response.parse()
            assert_matches_type(QuestionSet, question_set, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_set_id` but received ''"):
            await async_client.question_sets.with_raw_response.retrieve(
                question_set_id="",
            )

    @parametrize
    async def test_method_update_overload_1(self, async_client: AsyncSGPClient) -> None:
        question_set = await async_client.question_sets.update(
            question_set_id="question_set_id",
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    async def test_method_update_with_all_params_overload_1(self, async_client: AsyncSGPClient) -> None:
        question_set = await async_client.question_sets.update(
            question_set_id="question_set_id",
            instructions="instructions",
            name="name",
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    async def test_raw_response_update_overload_1(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.question_sets.with_raw_response.update(
            question_set_id="question_set_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question_set = await response.parse()
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    async def test_streaming_response_update_overload_1(self, async_client: AsyncSGPClient) -> None:
        async with async_client.question_sets.with_streaming_response.update(
            question_set_id="question_set_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question_set = await response.parse()
            assert_matches_type(QuestionSet, question_set, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_overload_1(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_set_id` but received ''"):
            await async_client.question_sets.with_raw_response.update(
                question_set_id="",
            )

    @parametrize
    async def test_method_update_overload_2(self, async_client: AsyncSGPClient) -> None:
        question_set = await async_client.question_sets.update(
            question_set_id="question_set_id",
            restore=True,
        )
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    async def test_raw_response_update_overload_2(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.question_sets.with_raw_response.update(
            question_set_id="question_set_id",
            restore=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question_set = await response.parse()
        assert_matches_type(QuestionSet, question_set, path=["response"])

    @parametrize
    async def test_streaming_response_update_overload_2(self, async_client: AsyncSGPClient) -> None:
        async with async_client.question_sets.with_streaming_response.update(
            question_set_id="question_set_id",
            restore=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question_set = await response.parse()
            assert_matches_type(QuestionSet, question_set, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_overload_2(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_set_id` but received ''"):
            await async_client.question_sets.with_raw_response.update(
                question_set_id="",
                restore=True,
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        question_set = await async_client.question_sets.list()
        assert_matches_type(AsyncCursorPage[QuestionSet], question_set, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        question_set = await async_client.question_sets.list(
            ending_before="ending_before",
            include_archived=True,
            limit=1,
            starting_after="starting_after",
            views=["questions"],
        )
        assert_matches_type(AsyncCursorPage[QuestionSet], question_set, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.question_sets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question_set = await response.parse()
        assert_matches_type(AsyncCursorPage[QuestionSet], question_set, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.question_sets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question_set = await response.parse()
            assert_matches_type(AsyncCursorPage[QuestionSet], question_set, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSGPClient) -> None:
        question_set = await async_client.question_sets.delete(
            "question_set_id",
        )
        assert_matches_type(QuestionSetDeleteResponse, question_set, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.question_sets.with_raw_response.delete(
            "question_set_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question_set = await response.parse()
        assert_matches_type(QuestionSetDeleteResponse, question_set, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSGPClient) -> None:
        async with async_client.question_sets.with_streaming_response.delete(
            "question_set_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question_set = await response.parse()
            assert_matches_type(QuestionSetDeleteResponse, question_set, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_set_id` but received ''"):
            await async_client.question_sets.with_raw_response.delete(
                "",
            )
