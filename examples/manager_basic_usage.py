import asyncio
from pathlib import Path

from tf2schema import SchemaManager


async def main():
    """
    An example of using the SchemaManager to fetch the schema and get the name of an item from its SKU.
    Schema is being saved to a file, so it will be fetched only once. Every subsequent run will use the saved schema.
    """
    steam_api_key = "change_me"

    async with SchemaManager(
            steam_api_key=steam_api_key,
            file_path=Path(__file__).parent / "schema.json",
            save_to_file=True
    ) as manager:
        # Wait until the schema is fetched
        await manager.wait_for_schema()

        sku = "30911;5;u144"
        item_name = manager.schema.get_name_from_sku(sku)

        print(f"Item name for SKU {sku}: {item_name}")
        # Expected output: "Item name for SKU 30911;5;u144: Snowblinded Fat Man's Field Cap"


if __name__ == "__main__":
    asyncio.run(main())
