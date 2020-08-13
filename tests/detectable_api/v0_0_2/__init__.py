from fastapi import APIRouter
from fastapi.requests import Request

parent_router = APIRouter()


@parent_router.get("/test")
def route(request: Request):
    return {"version": request.app.version}
