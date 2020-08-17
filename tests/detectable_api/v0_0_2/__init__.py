from fastapi.requests import Request
from semantic_version import Version

from fastapi_versioned import VersionRouter

version = VersionRouter(Version("0.0.2"))


@version.router.get("/test2")
def route(request: Request):
    return {"version": str(request.app.version)}
