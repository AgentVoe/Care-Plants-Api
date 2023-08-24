import datetime

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

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    login: str
    name: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class PlantSchema(PlantBase):
    users: list[UserBase]


class UsersSchema(UserBase):
    plants: list[PlantBase]


class WateringBase(BaseModel):
    week_day: int
    time: datetime
    last_watering: datetime


class Watering(WateringBase):
    id: int

    class Config:
        from_attributes = True


class WateringSchema(WateringBase):
    plants: list[PlantBase]
