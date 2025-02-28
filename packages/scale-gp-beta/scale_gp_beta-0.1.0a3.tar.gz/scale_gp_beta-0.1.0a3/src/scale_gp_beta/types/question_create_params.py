# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["QuestionCreateParams", "Choice", "NumberOptions", "RatingOptions"]


class QuestionCreateParams(TypedDict, total=False):
    prompt: Required[str]

    title: Required[str]

    type: Required[Literal["categorical", "free_text", "rating", "number"]]

    choices: Iterable[Choice]

    conditions: Iterable[Dict[str, object]]

    dropdown: bool

    multi: bool

    number_options: Annotated[NumberOptions, PropertyInfo(alias="numberOptions")]

    rating_options: Annotated[RatingOptions, PropertyInfo(alias="ratingOptions")]

    required: bool


class Choice(TypedDict, total=False):
    label: Required[str]

    value: Required[Union[str, bool, float]]

    audit_required: bool


class NumberOptions(TypedDict, total=False):
    max: float
    """Maximum value for the number"""

    min: float
    """Minimum value for the number"""


class RatingOptions(TypedDict, total=False):
    max_label: Required[Annotated[str, PropertyInfo(alias="maxLabel")]]
    """Maximum value for the rating"""

    min_label: Required[Annotated[str, PropertyInfo(alias="minLabel")]]
    """Minimum value for the rating"""

    scale_steps: Required[Annotated[int, PropertyInfo(alias="scaleSteps")]]
    """Number of steps in the rating scale"""
