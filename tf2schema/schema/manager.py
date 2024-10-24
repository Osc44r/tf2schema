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
    """
    Schema manager for fetching and storing the TF2 schema.
    """
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
        """Whether the schema has been fetched."""
        return self.schema is not None

    async def get(self,
                  *,
                  force_files: Optional[bool] = False) -> Schema:
        """
        Get the schema, fetching from Steam if necessary.

        :param force_files: Whether to force fetching from files.
        """
        try:
            schema = await self.get_schema_from_file()

        except FileNotFoundError as e:
            if force_files:
                raise e

            schema = None

        if force_files:
            return schema

        if schema is None or time.time() - schema.fetch_time > self.update_interval.total_seconds():
            return await self.fetch_schema()

        return schema

    async def wait_for_schema(self, timeout: Optional[int] = 30) -> None:
        """
        Wait for the schema to be fetched.

        :param timeout: The timeout in seconds.
        """
        start = time.time()
        while not self.has_schema:
            await asyncio.sleep(0.1)
            if time.time() - start > timeout:
                raise TimeoutError("Timed out waiting for schema")

    async def fetch_schema(self) -> Schema:
        """
        Fetch the schema from Steam and Github.

        :return: Schema object.
        """
        items, schema_overview, paint_kits, items_game = await asyncio.gather(
            self._fetch_items_from_steam(),
            self._fetch_overview(),
            self._fetch_paint_kits_from_github(),
            self._fetch_items_game_from_github()
        )

        self.schema = Schema({
            "schema": {
                **schema_overview,
                "items": items,
                "paintkits": paint_kits,
            },
            "items_game": items_game
        }, time.time())

        if self.save_to_file:
            await self._save_schema_to_file(self.schema.file_data)

        return self.schema

    async def get_schema_from_file(self) -> Schema:
        """
        Get the schema from the file.
        :return: Schema object.
        """
        data = await self._get_schema_from_file()
        self.schema = Schema(data['raw'], data['fetch_time'])

        return self.schema

    # HTTP calls
    async def _fetch_page(self, url: str,
                          *,
                          retries: Optional[int] = 5,
                          headers: Optional[dict] = None,
                          wait_time: Optional[float] = 2,
                          **kwargs) -> httpx.Response:
        """
        Fetch a page with retries.

        :param url: Page URL.
        :param retries: Number of retries.
        :param headers: Request headers.
        :param wait_time: Time to wait between retries.
        :param kwargs: Additional request arguments.
        :return: Response object.
        """
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
                    await asyncio.sleep(wait_time)
            raise e

    async def _fetch_items_from_steam(self) -> list:
        """Fetch items from the Steam API."""
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

    async def _fetch_paint_kits_from_github(self) -> dict:
        """Fetch paint kits from the TF2 Github repo."""
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

    async def _fetch_items_game_from_github(self) -> dict:
        """Fetch items_game from the TF2 Github repo."""
        url = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-TF2/master/tf/scripts/items/items_game.txt'

        response = await self._fetch_page(url)

        return vdf.loads(response.text)["items_game"]

    async def _fetch_overview(self) -> dict:
        """Fetch the schema overview from the Steam API."""
        url = "https://api.steampowered.com/IEconItems_440/GetSchemaOverview"
        params = {
            "key": self.steam_api_key,
            "language": "en"
        }

        response = await self._fetch_page(url, params=params)
        data = response.json()

        del data['status']

        return data

    # File operations
    async def _get_schema_from_file(self) -> dict:
        """Get the schema from the file."""
        if not self.file_path.exists():
            raise FileNotFoundError("Schema file not found")

        async with aiofiles.open(self.file_path, "r", encoding="utf-8") as f:
            content = await f.read()

        return json.loads(content)

    async def _save_schema_to_file(self, data: dict) -> None:
        """Save the schema to the file."""
        os.makedirs(self.file_path.parent, exist_ok=True)
        async with aiofiles.open(self.file_path, "w") as f:
            await f.write(json.dumps(data))
