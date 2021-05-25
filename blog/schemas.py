from typing import List

from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserShow(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config():
        orm_mode = True


class BlogShow(Blog):
    creator: UserShow

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str
