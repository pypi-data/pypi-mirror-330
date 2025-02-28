# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "QuestionSet",
    "Question",
    "QuestionChoice",
    "QuestionNumberOptions",
    "QuestionOverrideConfig",
    "QuestionRatingOptions",
]


class QuestionChoice(BaseModel):
    label: str

    value: Union[str, bool, float]

    audit_required: Optional[bool] = None


class QuestionNumberOptions(BaseModel):
    max: Optional[float] = None
    """Maximum value for the number"""

    min: Optional[float] = None
    """Minimum value for the number"""


class QuestionOverrideConfig(BaseModel):
    required: Optional[bool] = None
    """Whether the question is required. False by default."""


class QuestionRatingOptions(BaseModel):
    max_label: str = FieldInfo(alias="maxLabel")
    """Maximum value for the rating"""

    min_label: str = FieldInfo(alias="minLabel")
    """Minimum value for the rating"""

    scale_steps: int = FieldInfo(alias="scaleSteps")
    """Number of steps in the rating scale"""


class Question(BaseModel):
    id: str

    created_at: datetime

    created_by_user_id: str

    prompt: str

    title: str

    type: Literal["categorical", "free_text", "rating", "number"]

    choices: Optional[List[QuestionChoice]] = None

    conditions: Optional[List[Dict[str, object]]] = None

    dropdown: Optional[bool] = None

    multi: Optional[bool] = None

    number_options: Optional[QuestionNumberOptions] = FieldInfo(alias="numberOptions", default=None)

    object: Optional[Literal["question"]] = None

    override_config: Optional[QuestionOverrideConfig] = None
    """
    Specifies additional configurations to use for the question in the context of
    the question set. For example, `{required: true}` sets the question as required.
    Writes to the question_id_to_config field on the response
    """

    rating_options: Optional[QuestionRatingOptions] = FieldInfo(alias="ratingOptions", default=None)

    required: Optional[bool] = None


class QuestionSet(BaseModel):
    id: str

    created_at: datetime

    created_by_user_id: str

    name: str

    archived_at: Optional[datetime] = None

    instructions: Optional[str] = None

    object: Optional[Literal["question_set"]] = None

    questions: Optional[List[Question]] = None
    """Questions in the question set"""
