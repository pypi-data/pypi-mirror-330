# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ComputerScreenInteractionParams"]


class ComputerScreenInteractionParams(TypedDict, total=False):
    action: Required[Literal["screenshot", "cursor_position"]]
    """The screen action to perform."""
