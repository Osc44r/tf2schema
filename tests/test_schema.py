from tf2schema import Schema

DATA_SKUS_NAMES = {
    "30911;5;u144": "Snowblinded Fat Man's Field Cap",
    "30881;11": "Strange Croaking Hazard",
    "9258;5;uncraftable;td-31154": "Non-Craftable Unusual Taunt: Time Out Therapy Unusualifier",
    "341;5;u39": "Cauldron Bubbles A Rather Festive Tree",
    "30114;5;u87": "Frostbite Valley Forge",
    "199;15;w3;pk120": "Iron Wood Mk.II Shotgun (Field-Tested)",
    "30609;5;u3108": "Festivized Formation Taunt: The Killer Solo",
    "463;5;u3015": "Infernal Flames Taunt: The Schadenfreude",
    "382;5;u35": "Smoking Big Country",
    "996;6": "The Loose Cannon",
    "817;5;u13": "Burning Flames Human Cannonball",
    "30755;5;u263": "Forever And Forever! Berlin Brain Bowl",
    "31374;6": "Hazard Handler",
    "31374;3": "Vintage Hazard Handler",
    "160;3;u4": "Vintage Community Sparkle Lugermorph",
    "61;6;strange": "Strange Unique Ambassador",
    "5778;9": "Self-Made Duck Token",
    "267;5": "Unusual Haunted Metal Scrap",
    "5009;3": "Vintage Class Token - Pyro",
    "5020;6": "Name Tag"
}


def test_schema_creation(schema: Schema):
    assert isinstance(schema, Schema), "Schema is not an instance of Schema."
    assert schema.fetch_time, "Schema fetch time is not set."
    assert schema.raw, "Schema raw data is not set."
    assert schema.crate_series_list, "Schema crate series list is not set."
    assert schema.munition_crates_list, "Schema munition crates list is not set."
    assert schema.weapon_skins_list, "Schema weapon skins list is not set."
    assert schema.qualities, "Schema qualities list is not set."
    assert schema.effects, "Schema effects list is not set."
    assert schema.paint_kits, "Schema paint kits list is not set."
    assert schema.paints, "Schema paints list is not set."


def test_sku_to_name(schema: Schema):
    for sku, name in DATA_SKUS_NAMES.items():
        assert schema.get_name_from_sku(sku) == name, f"SKU {sku} does not match name {name}"


def test_name_to_sku(schema: Schema):
    for sku, name in DATA_SKUS_NAMES.items():
        assert schema.get_sku_from_name(name) == sku, f"Name {name} does not match SKU {sku}"



def test_mannco_supply_series_variants(schema: Schema):
    # Steam / Express-Load may return "Series #NN" names; these must resolve to the same SKU as "#NN".
    assert schema.get_sku_from_name("Mann Co. Supply Crate Series #59") == "5045;6;c59"
    assert schema.get_sku_from_name("Mann Co. Supply Crate Series #59") == schema.get_sku_from_name(
        "Mann Co. Supply Crate #59"
    )

    mun_series = schema.get_sku_from_name("Mann Co. Supply Munition Series #91")
    mun_plain = schema.get_sku_from_name("Mann Co. Supply Munition #91")
    assert mun_series == mun_plain
    assert str(mun_series).endswith(";c91")
