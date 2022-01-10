from starlette.testclient import TestClient


def test_get_all_users(test_client: TestClient):

    response = test_client.get("/users/")

    assert response.status_code == 200


def test_create_user(test_client: TestClient):
    payload = dict(
        email="test2@test.com",
        password="testpassword"
    )

    response = test_client.post(
        "/users/",
        json=payload,
    )

    print(response.json())

    assert response.status_code == 201
