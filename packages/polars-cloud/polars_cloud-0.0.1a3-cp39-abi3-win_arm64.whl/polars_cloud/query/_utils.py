from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

from polars._utils.cloud import prepare_cloud_plan
from polars.exceptions import ComputeError, InvalidOperationError

from polars_cloud.query.dst import ParquetDst

with contextlib.suppress(ImportError):  # Module not available when building docs
    from pathlib import Path

    import polars_cloud.polars_cloud as pc_core


if TYPE_CHECKING:
    from polars import LazyFrame

    from polars_cloud._typing import Engine, PlanTypePreference
    from polars_cloud.query.dst import Dst


def prepare_query(
    lf: LazyFrame,
    *,
    dst: str | Path | Dst,
    partition_by: None | str | list[str],
    broadcast_over: None | list[list[list[Path]]],
    distributed: None | bool,
    engine: Engine,
    plan_type: PlanTypePreference,
    shuffle_compression: bool,
    n_retries: int,
    **optimizations: bool,
) -> tuple[bytes, bytes]:
    """Parse query inputs as a serialized plan and settings object."""
    try:
        plan = prepare_cloud_plan(lf, **optimizations)
    except (ComputeError, InvalidOperationError) as exc:
        msg = f"invalid cloud plan: {exc}"
        raise ValueError(msg) from exc

    if isinstance(dst, (str, Path)):
        dst = ParquetDst(dst)

    if broadcast_over is not None and partition_by is not None:
        msg = "only 1 of 'partition_by' or 'broadcast_over' can be set"
        raise ValueError(msg)

    if plan_type == "dot":
        prefer_dot = True
    elif plan_type == "plain":
        prefer_dot = False
    else:
        msg = f"'plan_type' must be one of: {{'dot', 'plain'}}, got {plan_type!r}"
        raise ValueError(msg)

    if engine == "cpu":
        use_gpu = False
    elif engine == "gpu":
        msg = "GPU mode is not yet supported, consider opening an issue"
        raise ValueError(msg)
    else:
        msg = f"`engine` must be one of {{'cpu', 'gpu'}}, got {engine!r}"
        raise ValueError(msg)

    if isinstance(partition_by, str):
        partition_by = list(partition_by)

    settings = pc_core.serialize_query_settings(
        dst=dst,
        max_threads=None,
        use_gpu=use_gpu,
        partition_by=partition_by,
        broadcast_over=broadcast_over,
        distributed=distributed,
        prefer_dot=prefer_dot,
        shuffle_compression=shuffle_compression,
        n_retries=n_retries,
    )

    return plan, settings
