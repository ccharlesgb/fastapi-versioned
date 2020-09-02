from decimal import Decimal
from typing import Any, Dict, List, Optional, cast

from pydantic import BaseModel, EmailStr, Field, condecimal
from starlette.datastructures import State


class ResourceNotFoundError(Exception):
    """
    Raised when a resoruce is not found in the application
    """


class UserCommon(BaseModel):
    email: EmailStr = Field(...)
    # Example only. Never store passwords in plain-text
    # See: https://fastapi.tiangolo.com/tutorial/security/first-steps/
    password: str
    is_admin: bool


class User(UserCommon):
    id: int


class UserCreate(UserCommon):
    pass


class ProductCommon(BaseModel):
    id: int
    name: str = Field(..., max_length=128)
    stock_left: int = Field(..., ge=0)
    price: condecimal(multiple_of=Decimal("0.01"))


class Product(ProductCommon):
    id: int


class ProductCreate(ProductCommon):
    pass


class FakeDB:
    """
    Simple identity map data-structure so we don't have to set up a real DB for the example app
    Don't do this if you want persistence, use a real DB
    """

    def __init__(self):
        self.users: Dict[int, User] = {}
        self.products: Dict[int, Product] = {}


def get_new_key(id_map: Dict[int, Any]) -> int:
    try:
        return max(id_map.keys()) + 1
    except ValueError as e:
        if "arg is an empty sequence" in str(e):
            return 1
        else:
            raise


def get_fake_db(state: State) -> FakeDB:
    return cast(state.db, FakeDB)


def get_users(db: FakeDB, is_admin: Optional[bool] = None) -> List[User]:
    if is_admin is not None:
        all_users = filter(lambda user: user.is_admin == is_admin, db.users.values())
    else:
        all_users = db.users.values()
    return list(all_users)


def get_users_by_id(db: FakeDB, user_id: int) -> User:
    try:
        return db.users[user_id]
    except KeyError:
        raise ResourceNotFoundError(f"Could not find user with id={user_id}")


def add_user(db: FakeDB, user: UserCreate) -> User:
    new_id = get_new_key(db.users)
    new_user = User(
        id=new_id, email=user.email, password=user.password, is_admin=user.is_admin
    )
    db.users[new_id] = new_user
    return new_user


def modify_user(db: FakeDB, user_id: int, user: User) -> User:
    try:
        old_user = db.users[user_id]
    except KeyError:
        raise ResourceNotFoundError(f"Could not find user with id={user_id}")
    old_user.email = user.email
    old_user.password = user.password
    return old_user
