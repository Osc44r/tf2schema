import pytest

from tests.conftest import schema_manager
from tf2schema import SchemaManager, Schema


@pytest.mark.asyncio
async def test_schema_fetching(schema_manager: SchemaManager):
    assert schema_manager.has_schema, "Schema was not fetched."

    schema = schema_manager.schema

    assert isinstance(schema, Schema), "Schema is not an instance of Schema."
    assert schema.fetch_time, "Schema fetch time is not set."
    assert schema.raw, "Schema raw data is not set."


@pytest.mark.asyncio
async def test_get_schema_from_file(schema_manager):
    new_manager = SchemaManager(
        file_path=schema_manager.file_path,
        file_only_mode=True
    )

    schema = await new_manager.get_schema_from_file()

    assert isinstance(schema, Schema), "Schema is not an instance of Schema."
    assert schema.fetch_time, "Schema fetch time is not set."
    assert schema.raw, "Schema raw data is not set."
