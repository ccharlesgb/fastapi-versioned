from fastapi import APIRouter
from fastapi.requests import Request
from semantic_version import Version
from starlette.testclient import TestClient

from fastapi_versioned import FastAPIVersioned, VersionRouter

EXAMPLE_MESSAGE = {"message": "success"}


def test_create_single_version():
    version = VersionRouter(Version("0.0.1"))

    @version.router.get("/test")
    def version_route(request: Request):
        return {"version": str(request.app.version)}

    api = FastAPIVersioned(title="Test API", versions=[version])

    client = TestClient(api)

    response = client.get(f"/v0.0.1/test")
    assert response.status_code == 200
    assert response.json() == {"version": "0.0.1"}


def test_create_two_versions_no_base():
    version = VersionRouter(Version("0.0.1"))

    @version.router.get("/test")
    def version_route(request: Request):
        return EXAMPLE_MESSAGE

    version2 = VersionRouter(Version("0.0.2"))

    @version2.router.get("/test_new")
    def version_route2(request: Request):
        return EXAMPLE_MESSAGE

    api = FastAPIVersioned(title="Test API", versions=[version, version2])

    client = TestClient(api)

    # We shouldn't see any cross over here between routes
    response = client.get(f"/v0.0.1/test")
    assert response.status_code == 200
    assert response.json() == EXAMPLE_MESSAGE
    response = client.get(f"/v0.0.1/test_new")
    assert response.status_code == 404

    response = client.get(f"/v0.0.2/test")
    assert response.status_code == 404
    response = client.get(f"/v0.0.2/test_new")
    assert response.status_code == 200
    assert response.json() == EXAMPLE_MESSAGE


def test_create_two_versions_with_base():
    version = VersionRouter(Version("0.0.1"))

    @version.router.get("/test")
    def version_route(request: Request):
        return EXAMPLE_MESSAGE

    @version.router.get("/common_route")
    def version_route_common(request: Request):
        return {"detail": "common"}

    version2 = VersionRouter(Version("0.0.2"), base=version.without([version_route]))

    @version2.router.get("/test")
    def version_route2(request: Request):
        return {"detail": "overridden"}

    api = FastAPIVersioned(title="Test API", versions=[version, version2])

    client = TestClient(api)

    # We should have kept the common route but we should have overridden the "/test" route with our new method
    response = client.get(f"/v0.0.1/test")
    assert response.status_code == 200
    assert response.json() == EXAMPLE_MESSAGE
    response = client.get(f"/v0.0.1/common_route")
    assert response.status_code == 200
    assert response.json() == {"detail": "common"}

    response = client.get(f"/v0.0.2/test")
    assert response.status_code == 200
    assert response.json() == {"detail": "overridden"}
    response = client.get(f"/v0.0.2/common_route")
    assert response.status_code == 200
    assert response.json() == {"detail": "common"}


def test_create_two_versions_with_base_sub_router():
    version = VersionRouter(Version("0.0.1"))

    @version.router.get("/test")
    def version_route(request: Request):
        return EXAMPLE_MESSAGE

    sub_router = APIRouter()

    @sub_router.get("/first")
    def first_route():
        return EXAMPLE_MESSAGE

    @sub_router.get("/second")
    def second_route():
        return EXAMPLE_MESSAGE

    version.router.include_router(sub_router, prefix="/resource")

    version2 = VersionRouter(Version("0.0.2"), base=version.without([sub_router]))
    api = FastAPIVersioned(title="Test API", versions=[version, version2])

    client = TestClient(api)

    # The new API should have the sub router completed removed
    response = client.get(f"/v0.0.1/test")
    assert response.status_code == 200
    assert response.json() == EXAMPLE_MESSAGE
    response = client.get(f"/v0.0.1/resource/first")
    assert response.status_code == 200
    assert response.json() == EXAMPLE_MESSAGE
    response = client.get(f"/v0.0.1/resource/second")
    assert response.status_code == 200
    assert response.json() == EXAMPLE_MESSAGE

    response = client.get(f"/v0.0.2/test")
    assert response.status_code == 200
    assert response.json() == EXAMPLE_MESSAGE
    response = client.get(f"/v0.0.2/resource/first")
    assert response.status_code == 404
    response = client.get(f"/v0.0.2/resource/second")
    assert response.status_code == 404


def test_version_router_duplicate_route():
    vr = VersionRouter(Version("0.0.1"))

    @vr.router.get("/tests/")
    def test_1():
        return {"detail": "test"}

    @vr.router.get("/tests/")
    def test_2():
        return {"detail": "test2"}

    # These two aren't duplicated by method so shouldn't show up
    @vr.router.get("/other/")
    def test_3():
        return {"detail": "test2"}

    @vr.router.post("/other/")
    def test_4():
        return {"detail": "test2"}

    duplicate_endpoints = vr.duplicate_routes

    duplicated_key = ("/tests/", "GET")
    assert duplicated_key in duplicate_endpoints.keys()
    assert set(route.endpoint for route in duplicate_endpoints[duplicated_key]) == {
        test_1,
        test_2,
    }


def test_version_router_no_duplicate_route():
    vr = VersionRouter(Version("0.0.1"))

    @vr.router.get("/tests/")
    def test_1():
        return {"detail": "test"}

    @vr.router.post("/tests/")
    def test_2():
        return {"detail": "test2"}

    @vr.router.get("/other/")
    def test_3():
        return {"detail": "test2"}

    assert len(vr.duplicate_routes) == 0
