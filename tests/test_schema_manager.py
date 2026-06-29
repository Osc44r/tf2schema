import pytest
import httpx

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
async def test_fetch_paint_kits_handles_trailing_nul(monkeypatch):
    manager = SchemaManager()
    payload = (
        '"lang"\n'
        "{\n"
        '    "Tokens"\n'
        "    {\n"
        '        "9_100_field { field_number: 2 }"\t\t"Forest Fire"\n'
        '        "9_101_field { field_number: 2 }"\t\t"101: Should Skip"\n'
        "    }\n"
        "}\n"
        "\x00\n"
    )

    async def fetch_page(*args, **kwargs):
        return httpx.Response(200, text=payload)

    monkeypatch.setattr(manager, "_fetch_page", fetch_page)

    assert await manager._fetch_paint_kits_from_github() == {"100": "Forest Fire"}


@pytest.mark.asyncio
async def test_get_schema_from_file(schema_manager):
    new_manager = SchemaManager(
        file_path=schema_manager.file_path,
        file_only_mode=True
    )

    schema = new_manager.get_schema_from_file()

    assert isinstance(schema, Schema), "Schema is not an instance of Schema."
    assert schema.fetch_time, "Schema fetch time is not set."
    assert schema.raw, "Schema raw data is not set."
