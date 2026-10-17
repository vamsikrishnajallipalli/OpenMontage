"""Nominal duration for OpenMontage's sequential edit-decision cuts.

Cut in/out are offsets INTO the source asset, not positions on the final
composition timeline. The edit/compose stages concatenate primary cuts in
array order; overlays do not extend the composition runtime. Effects that
intentionally overlap adjacent shots may shorten the eventual export.
"""

from __future__ import annotations

import math
from typing import Any


def nominal_duration_seconds(cuts: list[dict[str, Any]]) -> float:
    """Estimate running time from source trims and playback speeds.

    Raises ValueError for malformed cuts instead of returning a misleading
    duration that could cause narration to be silently truncated.
    """
    if not isinstance(cuts, list) or not cuts:
        raise ValueError("No cuts defined in composition")

    primary: list[float] = []
    background: list[float] = []
    seen: set[str] = set()
    for index, cut in enumerate(cuts):
        if not isinstance(cut, dict):
            raise ValueError(f"Cut {index}: expected object")
        name = str(cut.get("id", index))
        if name in seen:
            raise ValueError(f"Duplicate cut id: {name}")
        seen.add(name)
        try:
            start = float(cut["in_seconds"])
            end = float(cut["out_seconds"])
            speed = float(cut.get("speed", 1))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Cut '{name}': missing or invalid in/out/speed") from exc
        if not all(math.isfinite(v) for v in (start, end, speed)):
            raise ValueError(f"Cut '{name}': non-finite timing value")
        if start < 0 or end <= start or speed < 0.1:
            raise ValueError(f"Cut '{name}': invalid source trim or playback speed")
        duration = (end - start) / speed
        layer = cut.get("layer", "primary")
        if layer == "primary":
            primary.append(duration)
        elif layer == "background":
            background.append(duration)
        elif layer != "overlay":
            raise ValueError(f"Cut '{name}': unknown layer {layer!r}")

    timeline = primary if primary else background
    if not timeline:
        raise ValueError("No primary/background cuts to establish runtime")
    return round(sum(timeline), 3)
