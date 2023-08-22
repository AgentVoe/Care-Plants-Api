from pydantic import BaseModel


class PlantBase(BaseModel):
    title: str
    description: str
    image: str
    privacy: bool


class PlantCreate(PlantBase):
    pass


class Plant(PlantBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    login: str
    name: str


class User(UserBase):
    id: int
    plants: list[Plant] = []

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
