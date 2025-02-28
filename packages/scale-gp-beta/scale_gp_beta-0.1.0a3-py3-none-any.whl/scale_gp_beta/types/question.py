# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Question", "Choice", "NumberOptions", "RatingOptions"]


class Choice(BaseModel):
    label: str

    value: Union[str, bool, float]

    audit_required: Optional[bool] = None


class NumberOptions(BaseModel):
    max: Optional[float] = None
    """Maximum value for the number"""

    min: Optional[float] = None
    """Minimum value for the number"""


class RatingOptions(BaseModel):
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

    choices: Optional[List[Choice]] = None

    conditions: Optional[List[Dict[str, object]]] = None

    dropdown: Optional[bool] = None

    multi: Optional[bool] = None

    number_options: Optional[NumberOptions] = FieldInfo(alias="numberOptions", default=None)

    object: Optional[Literal["question"]] = None

    rating_options: Optional[RatingOptions] = FieldInfo(alias="ratingOptions", default=None)

    required: Optional[bool] = None
