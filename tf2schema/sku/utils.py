# Shared template for item attributes
TEMPLATE = {
    "defindex": 0,
    "quality": 0,
    "craftable": True,
    "tradable": True,
    "killstreak": 0,
    "australium": False,
    "effect": None,
    "festive": False,
    "paintkit": None,
    "wear": None,
    "quality2": None,
    "craftnumber": None,
    "crateseries": None,
    "target": None,
    "output": None,
    "outputQuality": None,
    "paint": None
}


def from_string(sku: str) -> dict:
    """Convert SKU string to an item object."""
    attributes = TEMPLATE.copy()

    parts = sku.split(";")
    if parts and parts[0].isnumeric():
        attributes["defindex"] = int(parts.pop(0))
    if parts and parts[0].isnumeric():
        attributes["quality"] = int(parts.pop(0))

    for part in parts:
        attribute = part.replace("-", "")
        if attribute == "uncraftable":
            attributes["craftable"] = False
        elif attribute in {"untradeable", "untradable"}:
            attributes["tradable"] = False
        elif attribute == "australium":
            attributes["australium"] = True
        elif attribute == "festive":
            attributes["festive"] = True
        elif attribute == "strange":
            attributes["quality2"] = 11
        elif attribute.startswith("kt") and attribute[2:].isnumeric():
            attributes["killstreak"] = int(attribute[2:])
        elif attribute.startswith("u") and attribute[1:].isnumeric():
            attributes["effect"] = int(attribute[1:])
        elif attribute.startswith("pk") and attribute[2:].isnumeric():
            attributes["paintkit"] = int(attribute[2:])
        elif attribute.startswith("w") and attribute[1:].isnumeric():
            attributes["wear"] = int(attribute[1:])
        elif attribute.startswith("td") and attribute[2:].isnumeric():
            attributes["target"] = int(attribute[2:])
        elif attribute.startswith("n") and attribute[1:].isnumeric():
            attributes["craftnumber"] = int(attribute[1:])
        elif attribute.startswith("c") and attribute[1:].isnumeric():
            attributes["crateseries"] = int(attribute[1:])
        elif attribute.startswith("od") and attribute[2:].isnumeric():
            attributes["output"] = int(attribute[2:])
        elif attribute.startswith("oq") and attribute[2:].isnumeric():
            attributes["outputQuality"] = int(attribute[2:])
        elif attribute.startswith("p") and attribute[1:].isnumeric():
            attributes["paint"] = int(attribute[1:])

    return attributes


def from_object(item: dict) -> str:
    """Convert an item object to an SKU string."""
    parts = [str(item.get("defindex", 0)), str(item.get("quality", 0))]

    if item.get("effect"):
        parts.append(f"u{item['effect']}")
    if item.get("australium"):
        parts.append("australium")
    if not item.get("craftable", True):
        parts.append("uncraftable")
    if not item.get("tradable", True):
        parts.append("untradable")
    if item.get("wear"):
        parts.append(f"w{item['wear']}")
    if item.get("paintkit"):
        parts.append(f"pk{item['paintkit']}")
    if item.get("quality2") == 11:
        parts.append("strange")
    if item.get("killstreak"):
        parts.append(f"kt-{item['killstreak']}")
    if item.get("target"):
        parts.append(f"td-{item['target']}")
    if item.get("festive"):
        parts.append("festive")
    if item.get("craftnumber"):
        parts.append(f"n{item['craftnumber']}")
    if item.get("crateseries"):
        parts.append(f"c{item['crateseries']}")
    if item.get("output"):
        parts.append(f"od-{item['output']}")
    if item.get("outputQuality"):
        parts.append(f"oq{item['outputQuality']}")
    if item.get("paint"):
        parts.append(f"p{item['paint']}")

    return ";".join(parts)


def from_api(item: dict) -> str:
    """Convert an API item representation to a SKU string."""
    attributes = TEMPLATE.copy()
    attributes.update({
        "defindex": item["defindex"],
        "quality": item["quality"],
        "craftable": not item.get("flag_cannot_craft", False),
        "tradable": not item.get("flag_cannot_trade", False)
    })

    for attribute in item.get("attributes", []):
        defindex = int(attribute["defindex"])
        value = attribute.get("float_value", attribute.get("value"))
        if defindex == 2025:
            attributes["killstreak"] = value
        elif defindex == 2027:
            attributes["australium"] = bool(value)
        elif defindex == 134:
            attributes["effect"] = value
        elif defindex == 2053:
            attributes["festive"] = bool(value)
        elif defindex == 834:
            attributes["paintkit"] = value
        elif defindex == 749:
            attributes["wear"] = value
        elif defindex == 214 and item["quality"] == 5:
            attributes["quality2"] = value
        elif defindex == 229:
            attributes["craftnumber"] = value
        elif defindex == 187:
            attributes["crateseries"] = value
        elif 2000 <= defindex <= 2009 and "attributes" in attribute:
            for attr in attribute["attributes"]:
                if int(attr["defindex"]) == 2012:
                    attributes["target"] = attr["float_value"]
        elif attribute.get("is_output"):
            attributes["output"] = attribute["itemdef"]
            attributes["outputQuality"] = attribute["quantity"]
        elif defindex == 142:
            attributes["paint"] = value

    return from_object(attributes)


__all__ = [
    "from_string",
    "from_object",
    "from_api"
]
