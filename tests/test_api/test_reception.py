from httpx import AsyncClient
import pytest
import uuid


@pytest.mark.asyncio
async def test_create_reception(client: AsyncClient, employee_token, pvz_id):
    response = await client.post(
        "/api/reception/create",
        json={
            "pvz_id": pvz_id,
            "status": "in_progress"
        },
        headers={"Authorization": f"Bearer {employee_token}"}
    )

    assert response.status_code == 201
    
    data = response.json()

    assert data["pvz_id"] == pvz_id



@pytest.mark.asyncio
async def test_not_exist_pvz_id(client: AsyncClient, employee_token):
    response = await client.post(
        "/api/reception/create",
        json={
            "pvz_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "status": "in_progress"
        },
        headers={"Authorization": f"Bearer {employee_token}"}
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_status_reception(client: AsyncClient, employee_token, pvz_id):
    reception = await client.post(
        "/api/reception/create",
        json={
            "pvz_id": pvz_id,
            "status": "in_progress"
        },
        headers={"Authorization": f"Bearer {employee_token}"}
    )

    assert reception.status_code == 201
    
    data = reception.json()

    assert data["pvz_id"] == pvz_id

    response = await client.post(
        "/api/reception/create",
        json={
            "pvz_id": pvz_id,
            "status": "in_progress"
        },
        headers={"Authorization": f"Bearer {employee_token}"}
    )

    assert response.status_code == 400

    
@pytest.mark.asyncio
async def test_close_reception(client: AsyncClient, employee_token, pvz_id):
    reception= await client.post(
        "/api/reception/create",
        json={
            "pvz_id": pvz_id,
            "status": "in_progress"
        },
        headers={"Authorization": f"Bearer {employee_token}"}
    )

    assert reception.status_code == 201

    response = await client.put(
        f"/api/reception/close_reception/pvz/{pvz_id}",
        headers={"Authorization": f"Bearer {employee_token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "close"


@pytest.mark.asyncio
async def test_reception_detail(client: AsyncClient, moderator_token, pvz_id):
    response = await client.get(
        f"/api/reception/pvz/{pvz_id}/detail",
        headers={"Authorization": f"Bearer {moderator_token}"}
    )

    assert response.status_code == 200









    







