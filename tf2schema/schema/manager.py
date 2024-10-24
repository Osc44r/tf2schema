import asyncio
import json
import os
import time
from datetime import timedelta
from logging import getLogger
from pathlib import Path
from typing import Optional

import aiofiles
import httpx
from fake_useragent import UserAgent

from .schema import Schema

log = getLogger(__name__)


class SchemaManager:
    user_agent = UserAgent()

    def __init__(self,
                 *,
                 steam_api_key: Optional[str] = None,
                 file_path: Optional[Path] = None,
                 save_to_file: Optional[bool] = False,
                 update_interval: Optional[timedelta] = timedelta(days=1)
                 ):
        self.steam_api_key = steam_api_key
        self.file_path = file_path or Path().parent / "schema.json"
        self.save_to_file = save_to_file
        self.update_interval = update_interval

        self.schema: Optional[Schema] = None

    @property
    def has_schema(self) -> bool:
        return self.schema is not None

    async def fetch(self,
                    *,
                    force_files: Optional[bool] = False):
        if force_files:
            return await self.fetch_schema_from_file()

        return await self.fetch_schema_from_steam()

    async def wait_for_schema(self, timeout: Optional[int] = 30):
        start = time.time()
        while not self.has_schema:
            await asyncio.sleep(0.1)
            if time.time() - start > timeout:
                raise TimeoutError("Timed out waiting for schema")

    async def fetch_schema_from_steam(self) -> Schema:
        items = await self._fetch_items_from_steam()

    async def fetch_schema_from_file(self) -> Schema:
        data = await self._fetch_schema_from_file()
        self.schema = Schema(data)

        return self.schema

    async def _fetch_page(self, url: str,
                          *,
                          retries: Optional[int] = 5,
                          headers: Optional[dict] = None,
                          **kwargs):
        if not headers:
            headers = {"User-Agent": self.user_agent.chrome}

        request = httpx.Request("GET", url, **kwargs)
        async with httpx.AsyncClient(headers=headers) as client:
            for i in range(retries):
                try:
                    response = await client.send(request)

                    response.raise_for_status()

                    data = response.json()

                    if data is None:
                        raise ValueError("No data received")

                    return data

                except (httpx.HTTPStatusError, ValueError) as e:
                    log.error(f"Failed to fetch schema page: {e}")
            raise e

    async def _fetch_items_from_steam(self) -> list:
        if self.steam_api_key is None:
            raise ValueError("Steam API key is required to fetch schema from Steam")

        url = "https://api.steampowered.com/IEconItems_440/GetSchemaItems"
        params = {
            "key": self.steam_api_key,
            "language": "en"
        }
        data = await self._fetch_page(url, params=params)

        items = data["result"]["items"]
        while "next" in data["result"]:
            params["start"] = data["result"]["next"]
            data = await self._fetch_page(url, params=params)
            items += data["result"]["items"]

        return items

    async def _fetch_schema_from_file(self):
        if not self.file_path.exists():
            raise FileNotFoundError("Schema file not found")

        async with aiofiles.open(self.file_path, "r", encoding="utf-8") as f:
            content = await f.read()

        return json.loads(content)

    async def _save_schema_to_file(self, data: str):
        os.makedirs(self.file_path.parent, exist_ok=True)
        async with aiofiles.open(self.file_path, "w") as f:
            await f.write(data)
