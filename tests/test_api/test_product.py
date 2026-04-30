from httpx import AsyncClient
import pytest

from tests.helpers import create_product


@pytest.mark.asyncio
async def test_product_create(client: AsyncClient, employee_token, pvz_id, reception_id):
    response = await client.post(
        f"/api/product/create/pvz/{pvz_id}",
        json={
            "type": "электроника",
            "reception_id": reception_id
        },
        headers={"Authorization": f"Bearer {employee_token}"}
    )

    assert response.status_code == 201

    data = response.json()

    assert data["type"] == "электроника"
    assert data["reception_id"] == reception_id


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient, employee_token, pvz_id, reception_id):
    p1 = await create_product(client, employee_token, pvz_id, reception_id)
    p2 = await create_product(client, employee_token, pvz_id, reception_id)

    response = await client.delete(
        f"/api/product/pvz/{pvz_id}/delete",
        headers={"Authorization": f"Bearer {employee_token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Продукт успешно удален"
