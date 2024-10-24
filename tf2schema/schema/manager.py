from logging import getLogger
from typing import Optional

import httpx
from fake_useragent import UserAgent

log = getLogger(__name__)


class SchemaManager:
    user_agent = UserAgent()

    def __init__(self, steam_api_key: str):
        self.steam_api_key = steam_api_key
        self.schema = None

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

    async def fetch_from_steam(self):
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
