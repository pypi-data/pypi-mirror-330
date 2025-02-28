from abc import ABC, abstractmethod

from bitads_client.schemas import (
    PingResponse,
    GenerateMinerUrlResponse,
    SendServerLoadRequest,
    SendUserIpActivityRequest,
)


class BitAdsClient(ABC):
    """
    Abstract base client for interacting with the BitAds.ai API.
    """

    def __init__(self, base_url: str, **headers):
        self.base_url = base_url
        self.headers = headers

    @abstractmethod
    async def ping(self) -> PingResponse:
        pass

    @abstractmethod
    async def generate_miner_url(
        self, campaign_id: str
    ) -> GenerateMinerUrlResponse:
        pass

    @abstractmethod
    async def send_server_load(self, data: SendServerLoadRequest) -> None:
        pass

    @abstractmethod
    async def send_user_ip_activity(
        self, data: SendUserIpActivityRequest
    ) -> None:
        pass
