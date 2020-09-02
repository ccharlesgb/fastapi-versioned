from starlette.requests import Request

from fastapi_versioned import FastAPIVersioned


def get_parent_app(request: Request) -> FastAPIVersioned:
    return request.app.state.parent
