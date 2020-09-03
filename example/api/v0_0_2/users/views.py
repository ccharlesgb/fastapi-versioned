from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from example import core
from fastapi_versioned import FastAPIVersioned, get_parent_app

router = APIRouter()


@router.get("/", response_model=List[core.User], tags=["user"])
def get_all_users(
    is_admin: Optional[bool] = Query(None),
    parent_app: FastAPIVersioned = Depends(get_parent_app),
):
    """

    """
    return core.get_users(parent_app.state.db, is_admin=is_admin)


@router.delete("/{user_id}", response_model=core.User, tags=["user"])
def delete_user(user_id: int, parent_app: FastAPIVersioned = Depends(get_parent_app)):
    """

    """
    return core.delete_user_by_id(parent_app.state.db, user_id)
