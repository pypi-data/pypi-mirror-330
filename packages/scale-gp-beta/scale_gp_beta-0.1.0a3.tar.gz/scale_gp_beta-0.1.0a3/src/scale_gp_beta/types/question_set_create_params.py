# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "QuestionSetCreateParams",
    "Question",
    "QuestionQuestionCreateRequestWithConfig",
    "QuestionQuestionCreateRequestWithConfigChoice",
    "QuestionQuestionCreateRequestWithConfigNumberOptions",
    "QuestionQuestionCreateRequestWithConfigOverrideConfig",
    "QuestionQuestionCreateRequestWithConfigRatingOptions",
    "QuestionQuestionIDWithConfiguration",
    "QuestionQuestionIDWithConfigurationOverrideConfig",
]


class QuestionSetCreateParams(TypedDict, total=False):
    name: Required[str]

    questions: Required[List[Question]]
    """IDs of existing questions in the question set or new questions to create.

    You can also optionally specify configurations for each question. Example:
    [`question_id`, {'id': 'question_id2', 'configuration': {...}}, {'title': 'New
    question', ...}]
    """

    instructions: str
    """Instructions to answer questions"""


class QuestionQuestionCreateRequestWithConfigChoice(TypedDict, total=False):
    label: Required[str]

    value: Required[Union[str, bool, float]]

    audit_required: bool


class QuestionQuestionCreateRequestWithConfigNumberOptions(TypedDict, total=False):
    max: float
    """Maximum value for the number"""

    min: float
    """Minimum value for the number"""


class QuestionQuestionCreateRequestWithConfigOverrideConfig(TypedDict, total=False):
    required: bool
    """Whether the question is required. False by default."""


class QuestionQuestionCreateRequestWithConfigRatingOptions(TypedDict, total=False):
    max_label: Required[Annotated[str, PropertyInfo(alias="maxLabel")]]
    """Maximum value for the rating"""

    min_label: Required[Annotated[str, PropertyInfo(alias="minLabel")]]
    """Minimum value for the rating"""

    scale_steps: Required[Annotated[int, PropertyInfo(alias="scaleSteps")]]
    """Number of steps in the rating scale"""


class QuestionQuestionCreateRequestWithConfig(TypedDict, total=False):
    prompt: Required[str]

    title: Required[str]

    type: Required[Literal["categorical", "free_text", "rating", "number"]]

    choices: Iterable[QuestionQuestionCreateRequestWithConfigChoice]

    conditions: Iterable[Dict[str, object]]

    dropdown: bool

    multi: bool

    number_options: Annotated[QuestionQuestionCreateRequestWithConfigNumberOptions, PropertyInfo(alias="numberOptions")]

    override_config: QuestionQuestionCreateRequestWithConfigOverrideConfig
    """
    Specifies additional configurations to use for the question in the context of
    the question set. For example, `{required: true}` sets the question as required.
    Writes to the question_id_to_config field on the response
    """

    rating_options: Annotated[QuestionQuestionCreateRequestWithConfigRatingOptions, PropertyInfo(alias="ratingOptions")]

    required: bool


class QuestionQuestionIDWithConfigurationOverrideConfig(TypedDict, total=False):
    required: bool
    """Whether the question is required. False by default."""


class QuestionQuestionIDWithConfiguration(TypedDict, total=False):
    id: Required[str]

    override_config: QuestionQuestionIDWithConfigurationOverrideConfig
    """
    Specifies additional configurations to use for the question in the context of
    the question set. For example, `{required: true}` sets the question as required.
    Writes to the question_id_to_config field on the response
    """


Question: TypeAlias = Union[QuestionQuestionCreateRequestWithConfig, QuestionQuestionIDWithConfiguration, str]
