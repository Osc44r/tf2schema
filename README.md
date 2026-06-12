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

## CrateTF ownership and consumers

`tf2schema` owns low-level TF2 schema fetching, file-backed schema loading, SKU helpers, and schema lookup helpers. It does not own CrateTF catalog, inventory, pricing, recommendations, classifieds, or trade policy.

Current CrateTF consumers include:

- `schema-service`, which fetches and writes the shared schema file.
- `catalog-service`, `inventory-service`, `trade-api-service`, `trade-orchestrator-service`, `recommendations-service`, and `backpacktf-classifieds-service`, which read schema data directly or through `CrateTfLib` schema helpers.
- `CrateTfLib`, which wraps local schema cache, schema lookup, lootlist, collection, and catalog metadata helpers.

Compatibility rules:

- Preserve SKU parsing and rendering compatibility unless every catalog/inventory/trade consumer is migrated together.
- File-backed schema behavior matters in Docker because many services read a shared schema volume rather than fetching from Steam themselves.
- Do not move CrateTF service policy into this library; keep it as TF2 schema/domain utilities.
- Schema fetching can touch Steam and GitHub endpoints. Production service retries, leader election, and event publication belong in `schema-service`.

## Public API

Stable imports:

```python
from tf2schema import Schema, SchemaManager, sku
from tf2schema.sku import from_string, from_object, from_api
```

Public behavior:

- `SchemaManager` fetches schema data from Steam/GitHub or loads it from a local file.
- `Schema` resolves item names, SKUs, qualities, effects, crate series, paint kits, and related TF2 schema metadata.
- `tf2schema.sku` converts between TF2 SKU strings, item objects, and Steam API item representations.

These helpers are shared contract code. Changes to SKU rendering, file-backed loading, or schema lookup behavior must be treated as cross-service changes for catalog, inventory, trade, schema, recommendations, and classifieds consumers.

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
    uv run --with-requirements requirements.txt --with pytest pytest
    ```

The tests include checks for schema fetching, conversion from SKU to name, and vice versa.

For changes that affect SKU behavior, schema loading, or file-only mode, also run targeted tests in `schema-service`, `catalog-service`, `inventory-service`, and trade consumers as appropriate.

## Release rules

- Documentation-only changes do not require a version bump.
- Code releases use `setup.py` version.
- `CrateTfLib` pins `tf2schema-py`, so release `tf2schema` before updating `CrateTfLib` and dependent service images.
- Do not document real Steam API keys.

## Contributing

If you'd like to contribute to this package, feel free to submit a pull request or open an issue. Contributions are
always welcome!

## License

This project is licensed under the MIT License.
