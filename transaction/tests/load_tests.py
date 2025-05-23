import asyncio
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_load_create_transactions():
    async with AsyncClient(base_url="http://127.0.0.1:8000",headers={"Autorization":"your_api_key"}) as ac:
        tasks = []

        for i in range(2200,2300):
            payload = {
                "transaction_id": i,
                "user_id": 1000 + i,
                "amount": 50.0 + i,
                "currency": "USD",
                "timestamp": "2025-04-26T10:49:20.392Z"
            }
            tasks.append(ac.post("/transactions/", json=payload))

        responses = await asyncio.gather(*tasks)

    for response in responses:
        print(response.text)
        assert response.status_code == 200

