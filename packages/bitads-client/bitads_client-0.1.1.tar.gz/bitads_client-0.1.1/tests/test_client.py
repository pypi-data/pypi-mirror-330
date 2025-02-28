import pytest

from bitads_client import logger
from bitads_client.client.impl import AsyncBitAdsClient
from bitads_client.schemas import PingResponse, GenerateMinerUrlResponse


pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def client():
    """Fixture to initialize an AsyncBitAdsClient instance."""
    base_url = "https://prod-s.a.bitads.ai/api"
    return AsyncBitAdsClient(
        base_url=base_url,
        hot_key="5GEQ4ZkrXcz7y3HK8TAd4V9ZeERJKPNeF21EifKqCJRkZGaY",
        v="3.0.0",
    )


@pytest.mark.asyncio
async def test_subnet_validator_list_miner_do_request_ping(client):
    """Test that subnet_ping returns a valid response with validators."""
    response = await client.ping()
    logger.info(f"Response: {response}")
    assert response is not None
    assert isinstance(response, PingResponse)
    assert len(response.validators) > 0


@pytest.mark.asyncio
async def test_subnet_miner_list_validator_do_request_ping(client):
    """Test that subnet_ping returns a valid response with miners."""
    response = await client.ping()
    logger.info(f"Response: {response}")
    assert response is not None
    assert isinstance(response, PingResponse)
    assert len(response.miners) > 0


@pytest.mark.asyncio
async def test_get_miner_unique_url(client):
    """Test that get_miner_unique_id returns a valid response."""
    response = await client.generate_miner_url("m0fdo0x5nl2ae")
    assert response is not None
    assert isinstance(response, GenerateMinerUrlResponse)
