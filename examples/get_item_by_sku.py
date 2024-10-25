import asyncio

from tf2schema import SchemaManager


async def main():
    """
    This example demonstrates how to get an item from the schema using its sku.
    """
    steam_api_key = "change_me"

    async with SchemaManager(
            steam_api_key=steam_api_key,
    ) as manager:
        await manager.wait_for_schema()

        sku = "160;3;u4"
        item = manager.schema.get_item_by_sku(sku)

        print(f"Item for sku {sku}: {item}")
        # Expected output: "Item for sku 160;3;u4: Item for name 160;3;u4: {'name': 'TTG Max Pistol', 'defindex': 160, 'item_class': 'tf_weapon_pistol', 'item_type_name': 'Pistol', 'item_name': 'Lugermorph', ...}"


if __name__ == "__main__":
    asyncio.run(main())
