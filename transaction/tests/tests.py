import pytest
from httpx import AsyncClient
from transaction.main import app

@pytest.mark.asyncio
class TestTransactions:
    
    @pytest.mark.asyncio
    async def test_create_transaction(self):
        async with AsyncClient(base_url="http://127.0.0.1:8000",headers={"Autorization":"your_api_key"}) as ac:
            payload = {
                "transaction_id": 1,
                "user_id": 123,
                "amount": 150.5,
                "currency": "USD",
                "timestamp": "2025-04-26T10:49:20.392Z"
            }
            response = await ac.post("/transactions/", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert "task_id" in body
        assert body["message"] == "Transaction received"

    @pytest.mark.asyncio
    async def test_create_transaction_duplicate(self):
        async with AsyncClient(base_url="http://127.0.0.1:8000",headers={"Autorization":"your_api_key"}) as ac:
            payload = {
                "transaction_id": 1,
                "user_id": 123,
                "amount": 150.5,
                "currency": "USD",
                "timestamp": "2025-04-26T10:49:20.392Z"
            }
            response = await ac.post("/transactions/", json=payload)
        assert response.status_code == 400
        assert response.json()["detail"] == "Transaction with this ID already exists."

    @pytest.mark.asyncio
    async def test_create_transaction_invalid_payload(self):
        async with AsyncClient(base_url="http://127.0.0.1:8000",headers={"Autorization":"your_api_key"}) as ac:
            payload = {
                "user_id": 123,
                "amount": 100,
                "currency": "USD",
                "timestamp": "2025-04-26T10:49:20.392Z"
            }
            response = await ac.post("/transactions/", json=payload)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_multiple_transactions(self):
        async with AsyncClient(base_url="http://127.0.0.1:8000",headers={"Autorization":"your_api_key"}) as ac:
            for i in range(2, 5):
                payload = {
                    "transaction_id": i,
                    "user_id": 100 + i,
                    "amount": 50 * i,
                    "currency": "USD",
                    "timestamp": "2025-04-26T10:49:20.392Z"
                }
                response = await ac.post("/transactions/", json=payload)
                assert response.status_code == 200
                assert "task_id" in response.json()

    @pytest.mark.asyncio
    async def test_get_statistics(self):
        async with AsyncClient(base_url="http://127.0.0.1:8000",headers={"Autorization":"your_api_key"}) as ac:
            response = await ac.get("/statistics/")
        assert response.status_code == 200
        stats = response.json()
        assert "total_transactions" in stats
        assert "average_transaction_amount" in stats
        assert "top_transactions" in stats

    @pytest.mark.asyncio
    async def test_statistics_after_transactions(self):
        async with AsyncClient(base_url="http://127.0.0.1:8000",headers={"Autorization":"your_api_key"}) as ac:
            for i in range(5, 8):
                await ac.post("/transactions/", json={
                    "transaction_id": i,
                    "user_id": 1000 + i,
                    "amount": 100 * i,
                    "currency": "USD",
                    "timestamp": "2025-04-26T10:49:20.392Z"
                })
            
            response = await ac.get("/statistics/")
            stats = response.json()
            
            assert stats["total_transactions"] >= 3
            assert isinstance(stats["average_transaction_amount"], float)
            assert isinstance(stats["top_transactions"], list)

    @pytest.mark.asyncio
    async def test_delete_all_transactions(self):
        async with AsyncClient(base_url="http://127.0.0.1:8000",headers={"Autorization":"your_api_key"}) as ac:
            response = await ac.delete("/transactions/")
        assert response.status_code == 200
        assert response.json()["detail"] in ["All transactions deleted", "Error deleting data"]

    @pytest.mark.asyncio
    async def test_delete_and_check_statistics(self):
        async with AsyncClient(base_url="http://127.0.0.1:8000",headers={"Autorization":"your_api_key"}) as ac:
            await ac.delete("/transactions/")
            response = await ac.get("/statistics/")
            stats = response.json()
            assert stats["total_transactions"] == 0
            assert stats["average_transaction_amount"] == 0.0
            assert stats["top_transactions"] == []

    @pytest.mark.asyncio
    async def test_delete_on_empty_db(self):
        async with AsyncClient(base_url="http://127.0.0.1:8000",headers={"Autorization":"your_api_key"}) as ac:
            await ac.delete("/transactions/") 
            response = await ac.delete("/transactions/") 
            assert response.status_code == 200
