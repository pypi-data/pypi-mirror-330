# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["QuestionSetUpdateParams", "PartialQuestionSetRequestBase", "RestoreRequest"]


class PartialQuestionSetRequestBase(TypedDict, total=False):
    instructions: str
    """Instructions to answer questions"""

    name: str


class RestoreRequest(TypedDict, total=False):
    restore: Required[Literal[True]]
    """Set to true to restore the entity from the database."""


QuestionSetUpdateParams: TypeAlias = Union[PartialQuestionSetRequestBase, RestoreRequest]
