from typing import List, Dict, Any

from pydantic import BaseModel

from bitads_client import logger
from bitads_client.codes import APIErrorCodes


class APIResponse(BaseModel):
    errors: List[int]

    def process_errors(self):
        if self.errors and 200 not in self.errors:
            error_messages = [
                APIErrorCodes.get_error_message(code) for code in self.errors
            ]
            logger.error(f"API returned errors: {error_messages}")
            raise ValueError(f"API error(s): {error_messages}")


class Setting(BaseModel):
    name: str
    value: str


class Campaign(BaseModel):
    date_started: str
    created_at: str
    product_name: str
    product_unique_id: str
    validator_id: int
    date_approved: str
    company_registration_number: str
    status: int
    product_refund_period_duration: int
    country_of_registration: str
    updated_at: str
    product_link: str
    product_type: int
    countries_approved_for_product_sales: str
    product_link_domain: str
    id: str
    type: int
    store_name: str


class AllCampaign(BaseModel):
    product_unique_id: str
    status: int


class PingResponse(APIResponse):
    result: bool
    errors: List[int]
    miners: List[str]
    validators: List[str]
    settings: List[Setting]
    campaigns: List[Campaign]
    allCampaigns: List[AllCampaign]


class GenerateMinerUrlResponse(APIResponse):
    data: Dict[str, Any]


class SendServerLoadRequest(BaseModel):
    timestamp: str
    hostname: str
    load_average: Dict[str, float]


class SendUserIpActivityRequest(BaseModel):
    user_activity: Dict[str, List[Dict[str, Any]]]
