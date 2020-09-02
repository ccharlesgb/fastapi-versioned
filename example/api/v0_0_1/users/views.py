from typing import List

from fastapi import APIRouter, Depends

from example import core
from fastapi_versioned import FastAPIVersioned, get_parent_app

router = APIRouter()


@router.get("/", response_model=List[core.User], tags=["user"])
def get_all_users(parent_app: FastAPIVersioned = Depends(get_parent_app)):
    return core.get_users(parent_app.state.db)


@router.get("/{user_id}", response_model=core.User, tags=["user"])
def get_user(user_id: int, parent_app: FastAPIVersioned = Depends(get_parent_app)):
    return core.get_users_by_id(parent_app.state.db, user_id)


@router.post("/", response_model=core.User, tags=["user"])
def add_user(
    user: core.UserCreate, parent_app: FastAPIVersioned = Depends(get_parent_app)
):
    return core.add_user(parent_app.state.db, user)


@router.put("/{user_id}", response_model=core.User, tags=["user"])
def modify_user(
    user_id: int,
    user: core.UserCreate,
    parent_app: FastAPIVersioned = Depends(get_parent_app),
):
    return core.modify_user(parent_app.state.db, user_id, user)
