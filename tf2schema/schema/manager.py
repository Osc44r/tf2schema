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
import vdf
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

    async def get(self,
                  *,
                  force_files: Optional[bool] = False):
        if force_files:
            return await self.get_schema_from_file()

        return await self.fetch_schema_from_steam()

    async def wait_for_schema(self, timeout: Optional[int] = 30):
        start = time.time()
        while not self.has_schema:
            await asyncio.sleep(0.1)
            if time.time() - start > timeout:
                raise TimeoutError("Timed out waiting for schema")

    async def fetch_schema_from_steam(self) -> Schema:
        items = await self._fetch_items_from_steam()

    async def get_schema_from_file(self) -> Schema:
        data = await self._fetch_schema_from_file()
        self.schema = Schema(data)

        return self.schema

    async def _fetch_page(self, url: str,
                          *,
                          retries: Optional[int] = 5,
                          headers: Optional[dict] = None,
                          **kwargs) -> httpx.Response:
        if not headers:
            headers = {"User-Agent": self.user_agent.chrome}

        request = httpx.Request("GET", url, **kwargs)
        async with httpx.AsyncClient(headers=headers) as client:
            for i in range(retries):
                try:
                    response = await client.send(request)

                    response.raise_for_status()

                    if response.json() is None and response.text is None:
                        raise ValueError("No data received")

                    return response

                except (httpx.HTTPStatusError, ValueError) as e:
                    log.error(f"Failed to get schema page: {e}")
            raise e

    async def _fetch_items_from_steam(self) -> list:
        if self.steam_api_key is None:
            raise ValueError("Steam API key is required to get schema from Steam")

        url = "https://api.steampowered.com/IEconItems_440/GetSchemaItems"
        params = {
            "key": self.steam_api_key,
            "language": "en"
        }
        response = await self._fetch_page(url, params=params)

        data = response.json()

        items = data["result"]["items"]
        while "next" in data["result"]:
            params["start"] = data["result"]["next"]
            response = await self._fetch_page(url, params=params)
            data = response.json()
            items += data["result"]["items"]

        return items

    async def _fetch_paint_kits_from_github(self):
        url = "https://raw.githubusercontent.com/SteamDatabase/GameTracking-TF2/master/tf/resource/tf_proto_obj_defs_english.txt"
        response = await self._fetch_page(url)

        parsed = vdf.loads(response.text)

        protos = parsed["lang"]["Tokens"]
        paint_kits = []
        for proto, name in protos.items():
            parts = proto.split(' ', 1)[0].split('_')
            if len(parts) != 3 or parts[0] != "9":
                continue

            definition = parts[1]

            if name.startswith(definition + ':'):
                continue

            paint_kits.append({"id": definition, "name": name})

        paint_kits.sort(key=lambda x: int(x["id"]))

        paintkits_obj = {}
        for paint_kit in paint_kits:
            if paint_kit["name"] not in paintkits_obj.values():
                paintkits_obj[paint_kit["id"]] = paint_kit["name"]

        return paintkits_obj

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
