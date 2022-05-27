from pydantic import BaseModel


class PostResponse(BaseModel):
    status: int = 201
    data: dict = []
    meta: dict = []

    class Config:
        orm_mode = True


class PutResponse(BaseModel):
    status: int = 200
    data: dict = []
    meta: dict = []

    class Config:
        orm_mode = True


class GetResponse(BaseModel):
    status: int = 200
    data: dict = []
    meta: dict = []

    class Config:
        orm_mode = True
