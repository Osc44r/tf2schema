import asyncio
import os
import time
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
                 ):
        self.steam_api_key = steam_api_key
        self.file_path = file_path or Path().parent / "schema.json"
        self.save_to_file = save_to_file

        self.schema: Optional[Schema] = None

    @property
    def has_schema(self) -> bool:
        return self.schema is not None

    async def wait_for_schema(self, timeout: Optional[int] = 30):
        start = time.time()
        while not self.has_schema:
            await asyncio.sleep(0.1)
            if time.time() - start > timeout:
                raise TimeoutError("Timed out waiting for schema")

    async def fetch_from_steam(self):
        data = await self._fetch_from_steam()
        self.schema = Schema(data)

        if self.save_to_file:
            await self._save_to_file(data)

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

                    if "result" not in data:
                        raise ValueError("Invalid response")

                    return data

                except (httpx.HTTPStatusError, ValueError) as e:
                    log.error(f"Failed to fetch schema page: {e}")
            raise e

    async def _fetch_from_steam(self):
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

    async def _fetch_from_file(self):
        if not self.file_path.exists():
            raise FileNotFoundError("Schema file not found")

        async with aiofiles.open(self.file_path, "r") as f:
            return await f.read()

    async def _save_to_file(self, data: str):
        os.makedirs(self.file_path.parent, exist_ok=True)
        async with aiofiles.open(self.file_path, "w") as f:
            await f.write(data)
