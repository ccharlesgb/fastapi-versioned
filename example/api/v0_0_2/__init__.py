from fastapi.requests import Request
from semantic_version import Version
from fastapi_versioned import VersionRouter
from .. import v0_0_1

version = VersionRouter(Version("0.0.2"), base=v0_0_1.version.without([v0_0_1.route, v0_0_1.sub_router]))


@version.router.get("/test")
def route(request: Request):
    return {"version_new": str(request.app.version)}
