import asyncio
import os

import pytest
from dotenv import load_dotenv

from tf2schema import SchemaManager


@pytest.fixture(scope="session")
def session():
    """Load environment variables for the session."""
    load_dotenv()
    yield


@pytest.fixture(scope="session")
def steam_api_key(session):
    """Get the Steam API key from the environment."""
    key = os.getenv("STEAM_API_KEY")
    if not key:
        raise ValueError("STEAM_API_KEY is not set in the environment.")

    return key


@pytest.fixture(scope="session")
def event_loop():
    """Create an asyncio event loop for the session."""
    loop = asyncio.get_event_loop()

    yield loop

    loop.close()


@pytest.fixture(scope="session")
async def schema_manager(steam_api_key, tmp_path_factory):
    """Fixture to create and initialize the SchemaManager for testing."""
    temp_dir = tmp_path_factory.mktemp("test_schema")
    file_path = temp_dir / "schema.json"

    async with SchemaManager(
            steam_api_key=steam_api_key,
            file_path=file_path,
            save_to_file=True,
    ) as manager:
        await manager.wait_for_schema()

        yield manager


@pytest.fixture(scope="session")
async def schema(schema_manager):
    """Fixture to provide the fetched schema for the session."""
    return schema_manager.schema
