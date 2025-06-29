import pytest

from .conftest import async_client as ac, API_PREFIX

pytestmark = pytest.mark.anyio
CLASSES_PREFIX = API_PREFIX + "/classes/"

CLASS_ID = 1
CLASS_NUM_1 = 1
CLASS_NUM_2 = 2
CLASS_ID_PARAM = '{class_id}'


async def test_get_classes(ac):
    response = await ac.get(f'{CLASSES_PREFIX}')
    assert response.status_code == 200


async def test_create_class(ac):
    response = await ac.post(
        f'{CLASSES_PREFIX}create/',
        json={"class_num": CLASS_NUM_1}
    )
    await ac.post(
        f'{CLASSES_PREFIX}create/',
        json={"class_num": CLASS_NUM_2}
    )
    assert response.status_code == 201


async def test_get_class(ac):
    response = await ac.get(
        f'{CLASSES_PREFIX}',
        params={"value": CLASS_ID, "by_id": True},
    )
    assert response.status_code == 200

    response = await ac.get(
        f'{CLASSES_PREFIX}',
        params={"value": CLASS_NUM_1, "by_id": False},
    )
    assert response.status_code == 200


async def test_delete_class(ac):
    response = await ac.delete(
        f'{CLASSES_PREFIX}delete/{CLASS_ID_PARAM}/',
        params={"value": CLASS_ID, "by_id": True},
    )
    assert response.status_code == 204

    response = await ac.delete(
        f'{CLASSES_PREFIX}delete/{CLASS_ID_PARAM}/',
        params={"value": CLASS_NUM_2, "by_id": False},
    )
    assert response.status_code == 204
