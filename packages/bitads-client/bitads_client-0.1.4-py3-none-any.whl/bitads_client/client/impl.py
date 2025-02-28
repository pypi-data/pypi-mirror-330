import json
from typing import Optional, Dict, Any

import aiohttp

from bitads_client.client.base import BitAdsClient
from bitads_client.schemas import (
    PingResponse,
    GenerateMinerUrlResponse,
    SendServerLoadRequest,
    APIResponse,
    SendUserIpActivityRequest,
)


class AsyncBitAdsClient(BitAdsClient):
    """
    Asynchronous implementation of BitAdsClient using aiohttp.
    """

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                url,
                headers=self.headers,
                params=params,
                json=json_body,
            ) as response:
                try:
                    response_text = await response.text()
                    response_json = json.loads(response_text)
                except json.JSONDecodeError:
                    raise ValueError(
                        f"Invalid JSON response received from {url}: {response_text}"
                    )
                except Exception as e:
                    raise ValueError(
                        f"Unexpected error while parsing response from {url}: {e}"
                    )
                return response_json

    async def ping(self) -> PingResponse:
        response = await self._request("GET", "ping")
        result = PingResponse.model_validate(response)
        result.process_errors()
        return result

    async def generate_miner_url(
        self, campaign_id: str
    ) -> GenerateMinerUrlResponse:
        response = await self._request(
            "GET", f"generate_miner_url?{campaign_id}"
        )
        result = GenerateMinerUrlResponse.model_validate(response)
        result.process_errors()
        return result

    async def send_server_load(self, data: SendServerLoadRequest) -> None:
        response = await self._request(
            "POST", "send_server_load", json_body=data.model_dump(mode="json")
        )
        result = APIResponse.model_validate(response)
        result.process_errors()

    async def send_user_ip_activity(
        self, data: SendUserIpActivityRequest
    ) -> None:
        response = await self._request(
            "POST",
            "send_user_ip_activity",
            json_body=data.model_dump(mode="json"),
        )
        result = APIResponse.model_validate(response)
        result.process_errors()
