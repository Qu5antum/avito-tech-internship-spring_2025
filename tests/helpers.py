from httpx import AsyncClient
import uuid
from uuid import UUID


# get user token
async def get_token(client: AsyncClient, role: str):
    email = f"{uuid.uuid4()}@test.com"

    await client.post("/api/user/register", json={
        "email": email,
        "password": "123",
        "role": role,
    })

    login = await client.post("/api/user/login", data={
        "username": email,
        "password": "123"
    })

    return login.json()["access_token"]

# create pvz
async def create_pvz(client: AsyncClient, token: str):
    response = await client.post(
        "/api/pvz/create",
        json={"city": "Москва"},
        headers={"Authorization": f"Bearer {token}"}
    )

    return response.json()["id"]

# create reception
async def create_reception(client: AsyncClient, token: str, pvz_id: UUID):
    response = await client.post(
        "/api/reception/create",
        json={
            "pvz_id": pvz_id,
            "status": "in_progress"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    return response.json()["id"]