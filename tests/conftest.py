import asyncio
import os

import pytest
import pytest_asyncio
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
    # Create a new event loop for the session
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    yield loop

    loop.close()


@pytest_asyncio.fixture(scope="session")
async def schema_manager(steam_api_key, tmp_path_factory):
    """Fixture to create and initialize the SchemaManager for testing."""
    temp_dir = tmp_path_factory.mktemp("test_schema")
    file_path = temp_dir / "schema.json"

    # Initialize SchemaManager and use it as an async context manager
    async with SchemaManager(
            steam_api_key=steam_api_key,
            file_path=file_path,
            save_to_file=True,
    ) as manager:
        await manager.wait_for_schema(timeout=90)
        yield manager


@pytest.fixture(scope="session")
def schema(schema_manager):
    """Fixture to provide the fetched schema for the session."""
    return schema_manager.schema
