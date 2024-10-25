import asyncio
from pathlib import Path

from tf2schema import SchemaManager


async def main():
    """
    An example of using the SchemaManager to get the schema from a file and get the name of an item from its SKU.
    Steam API key is not required in this mode. The schema is fetched from the file only.
    If file does not exist, an exception will be raised.
    """
    async with SchemaManager(
            file_path=Path(__file__).parent / "schema.json",
            file_only_mode=True
    ) as manager:
        try:
            await manager.wait_for_schema()
        except FileNotFoundError:
            print("Schema file not found. Please make sure it exists.")
            return

        # Example: Get the name of an item from the schema using its SKU
        sku = "996;6"
        item_name = manager.schema.get_name_from_sku(sku)
        print(f"Item name for SKU {sku}: {item_name}")
        # Expected output: "Item name for SKU 996;6: The Loose Cannon"


if __name__ == "__main__":
    asyncio.run(main())
