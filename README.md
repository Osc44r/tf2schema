# tf2schema

tf2schema is a Python package for interacting with the Team Fortress 2 (TF2) Schema. It provides an easy-to-use
`SchemaManager` class that allows fetching, updating, and managing the TF2 Schema from Steam's API or from a local file.
The package includes features such as automatic updates, file-based schema storage, and async support for better
performance.

The library builds on the work from [python-tf2-utilities](https://github.com/dixon2004/python-tf2-utilities) but
extends it with additional features, including async fetch operations and more Pythonic naming conventions.

## Features

- Fetch the TF2 schema asynchronously from Steam's API or a local file.
- Automatic schema updates (optional).
- Pythonic snake_case naming for schema functions.
- Integration with file-based schema management for environments where file-only mode is preferred.
- Uses `httpx` for async HTTP requests.

## Installation

You can install the package using `pip`:

```bash
pip install tf2schema-py
```

Make sure your environment has the following dependencies installed:

- `httpx`
- `python-dotenv`
- `pytest`
- `pytest-asyncio`

## Usage

Head to the [Examples](examples) directory for a quick start guide on how to use the `SchemaManager` & `Schema` classes.

### Basic Example

By default, when using the `async with` syntax, the `SchemaManager` will start the auto-update loop. If you prefer not
to have auto-update enabled, you should manually call `fetch_schema` or `get` to fetch the schema.

Here’s a basic example of how to use the `SchemaManager`:

```python
import asyncio
from tf2schema import SchemaManager
from pathlib import Path


async def main():
    steam_api_key = "YOUR_STEAM_API_KEY"

    async with SchemaManager(
            steam_api_key=steam_api_key,
            file_path=Path(__file__).parent / "schema.json",
            save_to_file=True
    ) as manager:
        # Wait until the schema is fetched
        await manager.wait_for_schema()

        # Get the name of an item from the schema using its SKU
        sku = "30911;5;u144"
        item_name = manager.schema.get_name_from_sku(sku)
        print(f"Item name for SKU {sku}: {item_name}")
        # Expected output: "Item name for SKU 30911;5;u144: Snowblinded Fat Man's Field Cap"


if __name__ == "__main__":
    asyncio.run(main())
```

### Disabling Auto-Update

If you do **not** want auto-update to be enabled, you should avoid using `async with` to create the `SchemaManager`.
Instead, create an instance and manually fetch the schema.

```python
import asyncio
from tf2schema import SchemaManager
from pathlib import Path


async def main():
    steam_api_key = "YOUR_STEAM_API_KEY"

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
```

### Auto-Updating Schema

The `SchemaManager` supports an auto-update feature that checks for schema updates at regular intervals. If you want to
enable the auto-update loop explicitly, you can do so with the `run` method:

```python
import asyncio
from tf2schema import SchemaManager
from pathlib import Path


async def main():
    steam_api_key = "YOUR_STEAM_API_KEY"

    async with SchemaManager(
            steam_api_key=steam_api_key,
            file_path=Path(__file__).parent / "schema.json",
            save_to_file=True,
            update_interval=timedelta(hours=12)  # Update every 12 hours
    ) as manager:
        # The manager will automatically update the schema in the background
        await manager.wait_for_schema()

        # Example: Get the name for another item from the schema using its SKU
        sku = "817;5;u13"
        item_name = manager.schema.get_name_from_sku(sku)
        print(f"Item name for SKU {sku}: {item_name}")
        # Expected output: "Item name for SKU 817;5;u13: Burning Flames Human Cannonball"


if __name__ == "__main__":
    asyncio.run(main())
```

### File-Only Mode

If you want to use the package in environments where the schema should only be fetched from a file (e.g., in Docker
containers), you can enable `file_only_mode`:

```python
import asyncio
from tf2schema import SchemaManager
from pathlib import Path


async def main():
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
```

## Running Tests

To run the tests, you need to set the `STEAM_API_KEY` as an environment variable:

1. Create a `.env` file with your Steam API key:

    ```
    STEAM_API_KEY=your_steam_api_key_here
    ```

2. Run the tests using `pytest`:

    ```bash
    pytest
    ```

The tests include checks for schema fetching, conversion from SKU to name, and vice versa.

## Contributing

If you'd like to contribute to this package, feel free to submit a pull request or open an issue. Contributions are
always welcome!

## License

This project is licensed under the MIT License.