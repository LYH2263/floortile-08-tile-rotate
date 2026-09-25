from app.repositories import history, rooms, tiles
from app.services import estimate_service


def _clean_room(_room_id):
    return {"id": 1, "name": "客房", "length": 6.0, "width": 4.5, "data_quality": "clean"}


def _rect_tile(_tile_id):
    return {"id": 2, "name": "600x300", "tile_l": 0.6, "tile_w": 0.3, "data_quality": "clean"}


def test_rotate_falls_back_to_system_default(monkeypatch):
    monkeypatch.setattr(rooms, "get_room", _clean_room)
    monkeypatch.setattr(tiles, "get_tile", _rect_tile)
    monkeypatch.setattr("app.repositories.settings_repo.get_default_rotate", lambda: True)

    res = estimate_service.run_estimate(1, 2, 8.0, False, "", rotate=None)

    assert res["rotated"] is True
    assert res["layout"]["cols"] == 20
    assert res["layout"]["rows"] == 8
    assert res["run_id"] is None


def test_explicit_rotate_overrides_default(monkeypatch):
    monkeypatch.setattr(rooms, "get_room", _clean_room)
    monkeypatch.setattr(tiles, "get_tile", _rect_tile)
    monkeypatch.setattr("app.repositories.settings_repo.get_default_rotate", lambda: True)

    res = estimate_service.run_estimate(1, 2, 8.0, False, "", rotate=False)

    assert res["rotated"] is False
    assert res["layout"]["cols"] == 10
    assert res["layout"]["rows"] == 15


def test_saved_run_persists_rotation_flag(monkeypatch):
    monkeypatch.setattr(rooms, "get_room", _clean_room)
    monkeypatch.setattr(tiles, "get_tile", _rect_tile)
    saved = {}

    def fake_insert(room_id, tile_id, waste_pct, rotated, result, note):
        saved.update(rotated=rotated, result=result)
        return 7

    monkeypatch.setattr(history, "insert_run", fake_insert)

    res = estimate_service.run_estimate(1, 2, 8.0, True, "n", rotate=True)

    assert res["run_id"] == 7
    assert res["rotated"] is True
    assert saved["rotated"] is True
    assert saved["result"]["rotated"] is True
    assert saved["result"]["layout"]["grid_count"] == 160
    assert saved["result"]["order_count"] == res["order_count"]
