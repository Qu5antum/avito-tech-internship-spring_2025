from httpx import AsyncClient
import pytest
import uuid

from tests.helpers import get_token, create_pvz


@pytest.mark.asyncio
async def test_create_pvz_succes(client: AsyncClient, moderator_token):
    moderator_token = await get_token(client, "moderator")

    response = await client.post(
        "/api/pvz/create",
        json={"city": "Москва"},
        headers={"Authorization": f"Bearer {moderator_token}"}
    )

    assert response.status_code == 201

    data = response.json()

    assert data["city"] == "Москва"


@pytest.mark.asyncio
async def test_create_pvz_forbidden(client: AsyncClient):
    employee_token = await get_token(client, "employee")

    response = await client.post(
        "/api/pvz/create",
        json={"city": "Москва"},
        headers={"Authorization": f"Bearer {employee_token}"}
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_pvz_invalid_city(client: AsyncClient):
    moderator_token = await get_token(client, "moderator")

    response = await client.post(
        "/api/pvz/create",
        json={"city": "Лондон"},
        headers={"Authorization": f"Bearer {moderator_token}"}
    )

    assert response.status_code != 201