# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, TypedDict

__all__ = ["QuestionSetListParams"]


class QuestionSetListParams(TypedDict, total=False):
    ending_before: Optional[str]

    include_archived: bool

    limit: int

    starting_after: Optional[str]

    views: List[Literal["questions"]]
