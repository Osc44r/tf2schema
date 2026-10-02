"""Offline regressions for the 2026-10-01 schema and Haunted Hoard names."""

from copy import deepcopy
import json

import pytest

from tf2schema import Schema, SchemaManager


def raw_schema():
    return {
        "schema": {
            "items": [
                {"defindex": 5981, "name": "Halloween 2026 Case", "item_name": "Haunted Hoard Case", "item_quality": 6,
                 "item_class": "supply_crate", "item_type_name": "Supply Crate", "proper_name": False},
                {"defindex": 5982, "name": "Halloween 2026 Key", "item_name": "Haunted Hoard Key", "item_quality": 6,
                 "item_class": "tool", "item_type_name": "Tool", "proper_name": False},
            ],
            "qualities": {"unique": 6, "haunted": 13},
            "qualityNames": {"unique": "Unique", "haunted": "Haunted"},
            "attribute_controlled_attached_particles": [],
            "paintkits": {},
        },
        "items_game": {
            "items": {
                "5981": {"static_attrs": {"set supply crate series": "153"}},
                "5982": {"prefab": "eventkey"},
                "15013": {"prefab": "paintkit_weapon_scattergun",
                          "static_attrs": {"paintkit_proto_def_index": "1"}},
                "mouse_pressed_sound": "ui/item_hat_pickup.wav",
                "drop_sound": "ui/item_hat_drop.wav",
            },
        },
    }


def test_new_schema_roundtrips_without_scalar_item_metadata(tmp_path):
    upstream = raw_schema()
    original = deepcopy(upstream)
    schema = Schema(upstream, 123.0)
    path = tmp_path / "schema.json"
    path.write_text(json.dumps(schema.file_data))
    loaded = SchemaManager(file_path=path, file_only_mode=True).get_schema_from_file()
    assert loaded.crate_series_list["5981"] == 153
    assert loaded.weapon_skins_list == schema.weapon_skins_list
    assert "15013" in json.dumps(loaded.weapon_skins_list)
    assert upstream == original
    assert set(loaded.raw["items_game"]["items"]) == {"5981", "5982", "15013"}


def test_old_schema_keeps_raw_identity():
    raw = raw_schema()
    del raw["items_game"]["items"]["mouse_pressed_sound"]
    del raw["items_game"]["items"]["drop_sound"]
    assert Schema(raw, 123.0).raw is raw


@pytest.mark.parametrize("name,sku,canonical", [
    ("Haunted Hoard Case", "5981;6;c153", "Haunted Hoard Case #153"),
    ("Haunted Hoard Case #153", "5981;6;c153", "Haunted Hoard Case #153"),
    ("Haunted Hoard Key", "5982;6", "Haunted Hoard Key"),
])
def test_haunted_hoard_names_are_not_quality_prefixes(name, sku, canonical):
    schema = Schema(raw_schema(), 123.0)
    assert schema.get_sku_from_name(name) == sku
    assert schema.get_name_from_sku(sku) == canonical


def test_unknown_broken_item_is_not_silently_dropped():
    raw = raw_schema()
    raw["items_game"]["items"]["5981"] = "malformed"
    with pytest.raises(AttributeError):
        Schema(raw, 123.0)
