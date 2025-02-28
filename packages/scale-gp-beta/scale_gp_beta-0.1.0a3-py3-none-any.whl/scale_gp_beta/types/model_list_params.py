# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["ModelListParams"]


class ModelListParams(TypedDict, total=False):
    ending_before: Optional[str]

    limit: int

    model_vendor: Optional[
        Literal[
            "openai",
            "cohere",
            "vertex_ai",
            "anthropic",
            "azure",
            "gemini",
            "launch",
            "llmengine",
            "model_zoo",
            "bedrock",
        ]
    ]

    name: Optional[str]

    starting_after: Optional[str]
