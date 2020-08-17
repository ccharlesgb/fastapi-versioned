from fastapi import APIRouter
from fastapi.requests import Request
from semantic_version import Version

from fastapi_versioned import VersionRouter

version = VersionRouter(Version("0.0.1"))


@version.router.get("/test1")
def route(request: Request):
    return {"version": str(request.app.version)}
