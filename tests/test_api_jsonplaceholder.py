import logging

import pytest
import requests


logger = logging.getLogger(__name__)
BASE_URL = "http://jsonplaceholder.typicode.com"


@pytest.mark.api
def test_get_post_existente_retorna_estructura_esperada():
    logger.info("Consultando un post existente")
    response = requests.get(f"{BASE_URL}/posts/1", timeout=10)
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == 1
    assert body["userId"] == 1
    assert isinstance(body["title"], str)
    assert isinstance(body["body"], str)


@pytest.mark.api
def test_get_recurso_inexistente_retorna_404():
    logger.info("Consultando endpoint inexistente")
    response = requests.get(f"{BASE_URL}/invalid-endpoint", timeout=10)

    assert response.status_code == 404
    assert response.json() == {}


@pytest.mark.api
def test_post_crea_recurso_con_payload_valido():
    logger.info("Creando post con payload valido")
    payload = {
        "title": "Entrega final automation QA",
        "body": "Prueba automatizada con requests",
        "userId": 7,
    }

    response = requests.post(f"{BASE_URL}/posts", json=payload, timeout=10)
    body = response.json()

    assert response.status_code == 201
    assert body["id"] == 101
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]


@pytest.mark.api
def test_delete_recurso_existente_retorna_respuesta_exitosa():
    logger.info("Eliminando post existente")
    response = requests.delete(f"{BASE_URL}/posts/1", timeout=10)

    assert response.status_code == 200
    assert response.json() == {}
