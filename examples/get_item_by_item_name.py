import asyncio

from tf2schema import SchemaManager


async def main():
    """
    This example demonstrates how to get an item from the schema using its name.
    """
    steam_api_key = "change_me"

    async with SchemaManager(
            steam_api_key=steam_api_key,
    ) as manager:
        await manager.wait_for_schema()

        name = "Name Tag"
        item = manager.schema.get_item_by_item_name(name)

        print(f"Item for name {name}: {item}")
        # Expected output: "Item for name Name Tag: {'name': 'Name Tag', 'defindex': 5020, 'item_class': 'tool', ...}"


if __name__ == "__main__":
    asyncio.run(main())
