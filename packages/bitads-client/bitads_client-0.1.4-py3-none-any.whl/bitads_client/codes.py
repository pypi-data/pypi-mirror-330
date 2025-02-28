class APIErrorCodes:
    ERROR_MAP = {
        100: "Internal Server Error.",
        101: "You must register your account as a Miner or Validator "
        "on the BitAds website to mine or validate on Subnet 16. "
        "Visit https://bitads.ai and register.",
        102: "User Status Not Active.",
        103: "Not Active Campaign.",
        104: "Not Query Parameters.",
        105: "Not All Query Parameters.",
        106: "User is Not a Miner.",
        107: "Campaigns Not Found.",
        108: "COLD KEY is incorrect.",
        109: "HOT KEY or COLD KEY is not defined.",
    }

    @classmethod
    def get_error_message(cls, code: int) -> str:
        return cls.ERROR_MAP.get(code, f"Unknown error code: {code}")
