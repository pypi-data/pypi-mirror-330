# BitAds Client Library

![BitAds Logo](https://bitads.ai/logo.png)

## 🚀 Overview
BitAds Client is an asynchronous Python client for interacting with the **BitAds.ai API**. It allows users to integrate with the **BitAds network** to retrieve campaign details, validate miners, and interact with the BitAds infrastructure.

## 📦 Installation

Install the package using pip:

```sh
pip install bitads-client
```

## 🔧 Configuration

### Importing the Client
```python
from bitads_client.client.impl import AsyncBitAdsClient
```

### Initializing the Client
```python
client = AsyncBitAdsClient(
    base_url="https://prod-s.a.bitads.ai/api",
    hot_key="your-hot-key",
)
```

## 📡 API Usage

### ✅ **Ping BitAds API**
```python
import asyncio

async def main():
    response = await client.ping()
    print(response)
    await client.close()

asyncio.run(main())
```

### 🔗 **Generate Miner URL**
```python
async def main():
    response = await client.generate_miner_url("campaign_id")
    print(response.data)
    await client.close()

asyncio.run(main())
```

### 📊 **Send Server Load Data**
```python
from bitads_client.schemas import SendServerLoadRequest

async def main():
    data = SendServerLoadRequest(
        timestamp="2024-06-08 19:33:07",
        hostname="server1",
        load_average={"1min": 3.5, "5min": 4.2, "15min": 4.0},
    )
    await client.send_server_load(data)
    await client.close()

asyncio.run(main())
```

### 📡 **Send User IP Activity**
```python
from bitads_client.schemas import SendUserIpActivityRequest

async def main():
    data = SendUserIpActivityRequest(
        user_activity={
            "user1": [{"ip": "192.168.1.1", "date": "2024-06-08", "count": 5}]
        }
    )
    await client.send_user_ip_activity(data)
    await client.close()

asyncio.run(main())
```

## ✅ Running Tests
To run unit tests:
```sh
pytest tests/
```

## 📝 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 📬 Contact
For issues, please open a GitHub issue or contact support at [Discord](https://discord.com/channels/799672011265015819/1189234502669697064).

---
🚀 **Enjoy seamless integration with BitAds.ai!**

    