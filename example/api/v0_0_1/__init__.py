from fastapi import APIRouter
from fastapi.requests import Request
from semantic_version import Version

from fastapi_versioned import VersionRouter

version = VersionRouter(Version("0.0.1"))


@version.router.get("/test")
def route(request: Request):
    return {"version_old": str(request.app.version)}


@version.router.get("/")
def hello_world(request: Request):
    return {"message": "Hello World"}


sub_router = APIRouter()


@sub_router.get("/old_tech")
def legacy_route(request: Request):
    return {"message": "This is a legacy route!"}


version.router.include_router(sub_router, prefix="/legacy")
