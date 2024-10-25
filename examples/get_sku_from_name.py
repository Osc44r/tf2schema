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

        name = "Snowblinded Fat Man's Field Cap"
        sku = manager.schema.get_sku_from_name(name)

        print(f"SKU for item {name}: {sku}")
        # Expected output: "SKU for item Snowblinded Snowblinded Fat Man's Field Cap: 30911;5;u144"


if __name__ == "__main__":
    asyncio.run(main())
