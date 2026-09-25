from app.engines.tile_math import layout_preview, tile_count


def test_guest_room_600_waste8():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0)
    assert r["area_m2"] == 27.0
    assert r["raw_count"] == 75
    assert r["order_count"] == 81
    assert r["layout"]["cols"] == 10
    assert r["layout"]["rows"] == 8
    assert r["layout"]["grid_count"] == 80


def test_layout_preview_small_room():
    lp = layout_preview(2.5, 2.0, 0.6, 0.6)
    assert lp["cols"] == 5
    assert lp["rows"] == 4
    assert lp["grid_count"] == 20


def test_zero_waste():
    r = tile_count(3.0, 3.0, 1.0, 1.0, 0.0)
    assert r["raw_count"] == 9
    assert r["order_count"] == 9


def test_no_rotate_matches_previous_behavior():
    r = tile_count(6.0, 4.5, 0.6, 0.3, 8.0)
    assert r["rotated"] is False
    assert r["raw_count"] == 150
    assert r["order_count"] == 162
    assert r["layout"]["cols"] == 10
    assert r["layout"]["rows"] == 15
    assert r["layout"]["grid_count"] == 150


def test_rotate_swaps_edges_for_piece_and_grid():
    r = tile_count(6.0, 4.5, 0.6, 0.3, 8.0, rotate=True)
    assert r["rotated"] is True
    # swapped: cols along room length use tile_w=0.3, rows use tile_l=0.6
    assert r["layout"]["cols"] == 20
    assert r["layout"]["rows"] == 8
    assert r["layout"]["grid_count"] == 160
    # piece area is rotation-invariant, so area-method counts stay put
    assert r["piece_m2"] == round(0.6 * 0.3, 4)
    assert r["raw_count"] == 150
    assert r["order_count"] == 162


def test_rotate_square_tile_keeps_layout():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, rotate=True)
    assert r["rotated"] is True
    assert r["layout"]["cols"] == 10
    assert r["layout"]["rows"] == 8
