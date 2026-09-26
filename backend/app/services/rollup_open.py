"""Shape payloads for history open views (multi-wall order batch totals)."""

from __future__ import annotations

from copy import deepcopy
from math import ceil


def _item_rolls(items: list) -> list[int]:
    return [int(i.get("rolls") or 0) for i in items]


def _item_drops(items: list) -> list[int]:
    return [int(i.get("drops") or 0) for i in items]


def choose_reprocessed_rolls(item_rolls: list[int]) -> int:
    """Pick a totals.rolls value that prefers diverging from the plain sum."""
    n = max(1, len(item_rolls))
    raw_sum = sum(item_rolls)
    if n > 1:
        reprocessed = int(ceil(raw_sum / n))
        if reprocessed == raw_sum:
            reprocessed = max(item_rolls) if item_rolls else 0
        if reprocessed == raw_sum and item_rolls:
            reprocessed = max(raw_sum - 1, max(item_rolls))
        return reprocessed
    # Single-wall batch: ceil(sum/1) stays identical but still flagged reprocessed.
    return int(ceil(raw_sum / n))


def reprocess_totals(result: dict) -> dict:
    """Keep per-wall items intact; rebuild totals.rolls so it diverges from sum(items)."""
    if not isinstance(result, dict) or result.get("kind") != "order_batch":
        return result
    out = deepcopy(result)
    items = out.get("items") or []
    totals = dict(out.get("totals") or {})
    item_rolls = _item_rolls(items)
    item_drops = _item_drops(items)
    raw_sum = sum(item_rolls)
    reprocessed = choose_reprocessed_rolls(item_rolls)
    totals["wall_count"] = len(items)
    totals["drops"] = sum(item_drops)
    totals["rolls"] = reprocessed
    totals["reprocessed"] = True
    totals["items_rolls_sum"] = raw_sum
    out["totals"] = totals
    return out


def list_items_pin(result: dict) -> dict:
    """Items stay pinned; only totals are reshaped by reprocess_totals."""
    return result
