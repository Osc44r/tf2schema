import asyncio
from pathlib import Path

from tf2schema import SchemaManager


async def main():
    """
    An example of using the SchemaManager to fetch the schema and get the name of an item from its SKU.

    The `run()` method is not called, so the schema will not be automatically updated.
    """
    steam_api_key = "change_me"

    # Create the SchemaManager instance
    manager = SchemaManager(
        steam_api_key=steam_api_key,
        file_path=Path(__file__).parent / "schema.json",
        save_to_file=True
    )

    # Manually fetch the schema from Steam's API or file if it exists
    await manager.get()

    # Example: Get the name of an item from the schema using its SKU
    sku = "160;3;u4"
    item_name = manager.schema.get_name_from_sku(sku)
    print(f"Item name for SKU {sku}: {item_name}")
    # Expected output: "Item name for SKU 160;3;u4: Vintage Community Sparkle Lugermorph"


if __name__ == "__main__":
    asyncio.run(main())
