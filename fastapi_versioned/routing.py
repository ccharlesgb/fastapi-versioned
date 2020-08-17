from typing import List, Callable, Optional

from fastapi import APIRouter


def include_router(new_router: APIRouter, old_router: APIRouter, exclude: Optional[List[Callable]] = None):
    new_router.include_router(old_router)

    if exclude:
        to_exclude = []
        for route in new_router.routes:
            if route.endpoint in exclude:
                to_exclude.append(route)

        for excluded in to_exclude:
            new_router.routes.remove(excluded)

