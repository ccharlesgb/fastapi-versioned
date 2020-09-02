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
