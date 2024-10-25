import asyncio

from tf2schema import SchemaManager


async def main():
    """
    This example demonstrates how to get the name of an item from its SKU using the Schema.
    """
    steam_api_key = "change_me"

    async with SchemaManager(
            steam_api_key=steam_api_key,
    ) as manager:
        await manager.wait_for_schema()

        sku = "160;3;u4"
        item_name = manager.schema.get_name_from_sku(sku)
        print(f"Item name for SKU {sku}: {item_name}")
        # Expected output: "Item name for SKU 160;3;u4: Vintage Community Sparkle Lugermorph"


if __name__ == "__main__":
    asyncio.run(main())
