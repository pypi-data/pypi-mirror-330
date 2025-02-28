import re

import pytest
from pydantic import ValidationError

from bitads_client.codes import APIErrorCodes
from bitads_client.schemas import (
    PingResponse,
    GenerateMinerUrlResponse,
    APIResponse,
    SendServerLoadRequest,
    SendUserIpActivityRequest,
    Setting,
    Campaign,
    AllCampaign,
)


def test_ping_response_valid():
    data = {
        "result": True,
        "errors": [],
        "miners": ["miner1", "miner2"],
        "validators": ["validator1"],
        "settings": [{"name": "SALESmax", "value": "2000"}],
        "campaigns": [
            {
                "date_started": "2024-08-29 14:25:58",
                "created_at": "2024-08-29 14:25:58",
                "product_name": "Product A",
                "product_unique_id": "prod123",
                "validator_id": 5,
                "date_approved": "2024-08-29 14:11:54",
                "company_registration_number": "123456",
                "status": 1,
                "product_refund_period_duration": 1,
                "country_of_registration": "US",
                "updated_at": "2024-08-29 14:25:58",
                "product_link": "https://example.com/productA",
                "product_type": 1,
                "countries_approved_for_product_sales": '["US", "CA"]',
                "product_link_domain": "example.com",
                "id": "campaign1",
                "type": 1,
                "store_name": "Example Store",
            }
        ],
        "allCampaigns": [{"product_unique_id": "product1", "status": 1}],
    }
    response = PingResponse.model_validate(data)
    assert response.result is True
    assert response.errors == []
    assert len(response.miners) == 2
    assert isinstance(response.settings[0], Setting)
    assert isinstance(response.campaigns[0], Campaign)
    assert isinstance(response.allCampaigns[0], AllCampaign)


def test_ping_response_invalid():
    data = {"result": "invalid_bool"}  # Invalid data type
    with pytest.raises(ValidationError):
        PingResponse.model_validate(data)


def test_generate_miner_url_valid():
    data = {
        "data": {
            "link": "https://x.bitads.ai/miner1/url",
            "minerUniqueId": "miner1",
        },
        "errors": [],
    }
    response = GenerateMinerUrlResponse.model_validate(data)
    assert response.data["link"] == "https://x.bitads.ai/miner1/url"


def test_generate_miner_url_invalid():
    data = {
        "data": {"minerUniqueId": "miner1"}
    }  # Missing required field "link"
    with pytest.raises(ValidationError):
        GenerateMinerUrlResponse.model_validate(data)


def test_send_server_load_request_valid():
    data = {
        "timestamp": "2024-06-08 19:33:07",
        "hostname": "server1",
        "load_average": {"1min": 3.5, "5min": 4.2, "15min": 4.0},
    }
    request = SendServerLoadRequest.model_validate(data)
    assert request.hostname == "server1"


def test_send_server_load_request_invalid():
    data = {
        "timestamp": "2024-06-08 19:33:07",
        "hostname": "server1",
    }  # Missing "load_average"
    with pytest.raises(ValidationError):
        SendServerLoadRequest.model_validate(data)


def test_send_user_ip_activity_request_valid():
    data = {
        "user_activity": {
            "user1": [{"ip": "192.168.1.1", "date": "2024-06-08", "count": 5}]
        }
    }
    request = SendUserIpActivityRequest.model_validate(data)
    assert request.user_activity["user1"][0]["ip"] == "192.168.1.1"


def test_send_user_ip_activity_request_invalid():
    data = {"user_activity": "invalid_format"}  # Should be a dictionary
    with pytest.raises(ValidationError):
        SendUserIpActivityRequest.model_validate(data)


def test_api_response_process_errors():
    code = 100
    response = APIResponse(errors=[code])

    expected_error_message = (
        f"API error(s): {[APIErrorCodes.get_error_message(code)]}"
    )

    with pytest.raises(
        ValueError,
        match=re.escape(expected_error_message),
    ):
        response.process_errors()


def test_api_response_no_errors():
    response = APIResponse(errors=[])
    assert response.errors == []
