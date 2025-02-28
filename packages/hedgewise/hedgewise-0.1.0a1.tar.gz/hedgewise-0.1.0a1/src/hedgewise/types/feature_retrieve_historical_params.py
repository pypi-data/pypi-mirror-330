# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["FeatureRetrieveHistoricalParams"]


class FeatureRetrieveHistoricalParams(TypedDict, total=False):
    add_strength_for_commodity: Optional[str]
    """
    If a future symbol is provided and a model for that commodity exists, a signed
    strength indicator will be returned in addition to the feature value
    """

    end_date: Optional[str]
    """End of feature data window (YYYY-MM-DD)"""

    start_date: Optional[str]
    """Start of feature data window (YYYY-MM-DD)"""
