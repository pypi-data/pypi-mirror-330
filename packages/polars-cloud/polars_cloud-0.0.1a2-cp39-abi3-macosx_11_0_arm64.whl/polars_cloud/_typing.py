"""Internal typing module.

Contains type aliases intended for private use.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

Engine: TypeAlias = Literal["cpu", "gpu"]
PlanTypePreference = Literal["dot", "plain"]

Json: TypeAlias = dict[str, Any]
PlanType: TypeAlias = Literal["physical", "ir"]
FileType: TypeAlias = Literal["none", "parquet", "ipc", "csv", "ndjson", "json"]
