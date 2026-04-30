from httpx import AsyncClient
import pytest
from uuid import UUID
import uuid



@pytest.mark.asyncio
async def test_create_pvz_succes(client: AsyncClient):
    email = f"{uuid.uuid4()}@test.com"

    register = await client.post(
        "/api/user/register",
        json={
            "email": email,
            "password": "123",
            "role": "moderator",
        }
    )

    assert register.status_code == 201

    login = await client.post(
        "/api/user/login",
        data = {
            "username": email,
            "password": "123"
        }
    )

    assert login.status_code == 201

    token = login.json()["access_token"]

    response = await client.post(
        "/api/pvz/create",
        json={"city": "Москва"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201

    data = response.json()

    assert data["city"] == "Москва"


@pytest.mark.asyncio
async def test_create_pvz_forbidden(client: AsyncClient):
    email = f"{uuid.uuid4()}@test.com"

    register = await client.post(
        "/api/user/register",
        json={
            "email": email,
            "password": "123",
            "role": "employee",
        }
    )

    assert register.status_code == 201

    login = await client.post(
        "/api/user/login",
        data = {
            "username": email,
            "password": "123"
        }
    )

    assert login.status_code == 201

    token = login.json()["access_token"]

    response = await client.post(
        "/api/pvz/create",
        json={"city": "Москва"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_pvz_invalid_city(client: AsyncClient):
    email = f"{uuid.uuid4()}@test.com"

    register = await client.post(
        "/api/user/register",
        json={
            "email": email,
            "password": "123",
            "role": "moderator",
        }
    )

    assert register.status_code == 201

    login = await client.post(
        "/api/user/login",
        data = {
            "username": email,
            "password": "123"
        }
    )

    assert login.status_code == 201

    token = login.json()["access_token"]

    response = await client.post(
        "/api/pvz/create",
        json={"city": "Лондон"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code != 201