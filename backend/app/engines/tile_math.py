"""Floor tile order count: area method + optional grid layout preview."""

from app.engines.helpers import ceil_units


def effective_dims(tile_l: float, tile_w: float, rotate: bool = False) -> tuple[float, float]:
    """Edge lengths actually laid along room length/width; rotate=90° swaps them."""
    if rotate:
        return float(tile_w), float(tile_l)
    return float(tile_l), float(tile_w)


def tile_count(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
    waste_pct: float,
    rotate: bool = False,
) -> dict:
    """
    raw_count: ceil(room_area / tile_piece_area)
    order_count: ceil(raw * (1 + waste_pct/100))
    rotate=True lays tiles turned 90°: piece/grid use swapped edge lengths.
    """
    eff_l, eff_w = effective_dims(tile_l, tile_w, rotate)
    area = float(room_l) * float(room_w)
    piece = eff_l * eff_w
    if piece <= 0 or area < 0:
        raise ValueError("invalid dimensions")
    raw = ceil_units(area / piece)
    with_waste = ceil_units(raw * (1 + float(waste_pct) / 100.0))
    layout = layout_preview(room_l, room_w, eff_l, eff_w)
    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "waste_pct": float(waste_pct),
        "order_count": with_waste,
        "rotated": bool(rotate),
        "layout": layout,
    }


def layout_preview(room_l: float, room_w: float, tile_l: float, tile_w: float) -> dict:
    """Grid count if tiles are laid on a full rectangular lattice (may exceed area method).

    tile_l/tile_w are the effective edge lengths along room length/width —
    callers pass swapped values when the tile is rotated 90°.
    """
    cols = ceil_units(float(room_l) / float(tile_l))
    rows = ceil_units(float(room_w) / float(tile_w))
    grid_count = cols * rows
    return {
        "cols": cols,
        "rows": rows,
        "grid_count": grid_count,
    }
