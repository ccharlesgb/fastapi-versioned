from fastapi.requests import Request
from starlette.testclient import TestClient

from fastapi_versioned import FastAPIParent
from fastapi import APIRouter
from .detectable_api import routers as detected_routers
from semantic_version import Version

router = APIRouter()


@router.get("/test")
def version_route(request: Request):
    return {"version": request.app.version}


def test_create_single_version():
    api = FastAPIParent(title="Test API")

    api.add_version(Version("0.0.1"), router)
    api.add_version(Version("0.0.2"), router)

    client = TestClient(api)
    for prefix in ["v0.0.1", "v0.0.2"]:
        response = client.get(f"/{prefix}/test")
        assert response.status_code == 200
        assert response.json() == {"version": prefix}


def test_version_detection():
    api = FastAPIParent(title="Test API")

    for prefix, version_router in detected_routers.items():
        api.add_version(prefix, version_router)

    client = TestClient(api)
    for prefix in ["v0.0.1", "v0.0.2"]:
        response = client.get(f"/{prefix}/test")
        assert response.status_code == 200
        assert response.json() == {"version": prefix}
