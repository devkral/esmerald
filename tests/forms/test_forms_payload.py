from dataclasses import dataclass
from typing import Any, Dict

from pydantic import BaseModel
from pydantic.dataclasses import dataclass as pydantic_dataclass

from esmerald import Form, Gateway, post
from esmerald.testclient import create_client


@pydantic_dataclass
class User:
    id: int
    name: str


@dataclass
class UserOut:
    id: int
    name: str


class UserModel(BaseModel):
    id: int
    name: str


@post("/form")
async def test_form(payload: Any = Form()) -> Dict[str, str]:
    return {"name": payload["name"]}


@post("/complex-form-pydantic")
async def test_complex_form_pydantic_dataclass(payload: User = Form()) -> User:
    return payload


@post("/complex-form-dataclass")
async def test_complex_form_dataclass(payload: UserOut = Form()) -> UserOut:
    return payload


@post("/complex-form-basemodel")
async def test_complex_form_basemodel(payload: UserModel = Form()) -> UserModel:
    return payload


def test_send_form(test_client_factory):
    payload = {"name": "Test"}

    with create_client(routes=[Gateway(handler=test_form)]) as client:
        response = client.post("/form", data=payload)

        assert response.status_code == 201
        assert response.json() == {"name": "Test"}


def test_send_complex_form_pydantic_dataclass(test_client_factory):
    payload = {"id": 1, "name": "Test"}
    with create_client(
        routes=[Gateway(handler=test_complex_form_pydantic_dataclass)],
        enable_openapi=True,
    ) as client:
        response = client.post("/complex-form-pydantic", data=payload)
        assert response.status_code == 201, response.text
        assert response.json() == {"id": 1, "name": "Test"}


def test_send_complex_form_normal_dataclass(test_client_factory):
    payload = {"id": 1, "name": "Test"}
    with create_client(
        routes=[Gateway(handler=test_complex_form_dataclass)],
        enable_openapi=True,
    ) as client:
        response = client.post("/complex-form-dataclass", data=payload)
        assert response.status_code == 201, response.text
        assert response.json() == {"id": 1, "name": "Test"}


def test_send_complex_form_base_model(test_client_factory):
    payload = {"id": 1, "name": "Test"}
    with create_client(
        routes=[Gateway(handler=test_complex_form_basemodel)],
        enable_openapi=True,
    ) as client:
        response = client.post("/complex-form-basemodel", data=payload)
        assert response.status_code == 201, response.text
        assert response.json() == {"id": 1, "name": "Test"}
