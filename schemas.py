import datetime

from pydantic import BaseModel


class PlantBase(BaseModel):
    title: str
    description: str
    image: str
    privacy: bool


class Plant(PlantBase):
    id: int

    class Config:
        from_attributes = True


class PlantCreate(PlantBase):
    pass


class PlantUpdate(PlantBase):
    pass
    # class Config:
    #     schema_extra = {
    #         "title": "title",
    #         "description": "description",
    #         "image": "image",
    #         "privacy": "privacy"
    #     }


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
    time: datetime.date
    last_watering: datetime.date


class Watering(WateringBase):
    id: int

    class Config:
        from_attributes = True


class WateringSchema(WateringBase):
    plants: list[PlantBase]


class UserPlantBase(BaseModel):
    user_id: int
    plant_id: int


class UserPlant(UserPlantBase):
    id: int

    class Config:
        from_attributes = True