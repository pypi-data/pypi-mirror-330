from sipametrics.endpoints import PUBLIC_API_VERSION, SOURCE
from typing import Dict
import asyncio
import aiohttp
import json


class BaseClient:
    def __init__(self, api_key: str, api_secret: str):
        self.session = aiohttp.ClientSession()
        self.USER_API_KEY = api_key
        self.USER_API_SECRET = api_secret

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, tb):
        await self.session.close()

    async def _get(self, path, **kwargs):
        return await self._request_api("get", path, **kwargs)

    async def _post(self, path, **kwargs) -> Dict:
        return await self._request_api("post", path, **kwargs)

    async def _request_api(self, method, path, **kwargs) -> Dict:
        uri = path
        return await self._request(method, uri, **kwargs)

    def _generate_auth_headers(self, method) -> Dict:
        if method.upper() == "GET":
            return {
                "X-API-KEY": self.USER_API_KEY,
                "X-API-SECRET": self.USER_API_SECRET,
                "X-Source": f"{SOURCE}-{PUBLIC_API_VERSION}",
            }
        elif method.upper() == "POST":
            return {
                "X-Source": f"{SOURCE}-{PUBLIC_API_VERSION}",
                "X-API-KEY": self.USER_API_KEY,
                "X-API-SECRET": self.USER_API_SECRET,
                "Content-Type": "application/json",
            }
        else:
            return {}

    async def _request(self, method: str, uri: str, **kwargs) -> Dict:
        headers = {}

        if method.upper() in ["POST", "GET"]:
            headers.update(self._generate_auth_headers(method))

        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"])

        query_params = kwargs.pop("params", None)
        async with getattr(self.session, method)(
            uri,
            params=query_params,
            headers=headers,
            data=kwargs.get("data"),
        ) as response:
            return await self._handle_response(response)

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict:
        """
        Handles retries for transient errors and processes API responses.
        """
        retries = 3
        delay = 2
        for attempt in range(retries):
            if response.status == 200:
                try:
                    return await response.json()
                except aiohttp.ContentTypeError as e:
                    raise ValueError("Invalid JSON response") from e
            elif response.status in [500, 502, 503, 504]:
                await asyncio.sleep(delay)
                delay *= 2
            else:
                response.raise_for_status()

        raise Exception(f"Failed to process response after {retries} retries. Status: {response.status}")
