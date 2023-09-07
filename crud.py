from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, text, and_

import crud
import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).options(joinedload(models.User.plants)).where(models.User.id == user_id).one()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_psswrd = user.password + "123"
    db_user = models.User(name=user.name, login=user.login, password=fake_hashed_psswrd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_plant(db: Session, plant: schemas.PlantCreate, login: str):
    plant_to_add = models.Plant(
        title=plant.title,
        description=plant.description,
        image=plant.image,
        privacy=plant.privacy
    )

    db.add(plant_to_add)
    db.commit()
    db.refresh(plant_to_add)
    user_id = get_user_by_login(db=db, login=login)
    add_user_plant_row(db=db, user_id=user_id.id, plant_id=plant_to_add.id)
    return plant_to_add


def get_user_by_login(db: Session, login: str):
    user = db.query(models.User).options(joinedload(models.User.plants)).where(models.User.login == login).first()
    if user is None:
        return None
    return user


def get_user_plants(db: Session, login: str):
    plants = db.query(models.User).options(joinedload(models.User.plants)).where(models.User.login == login)
    return plants


def get_alike_plants(db: Session, user_login: str, plant_title: str):
    res = db.query(models.Plant).join(models.UserPlant, models.Plant.id == models.UserPlant.plant_id).\
        join(models.User, models.User.id == models.UserPlant.user_id).\
        where(and_(models.User.login == user_login, models.Plant.title == plant_title))
    return res


def add_user_plant_row(db: Session, user_id: int, plant_id: int):
    user_plant_to_add = models.UserPlant(
        user_id=user_id,
        plant_id=plant_id
    )

    db.add(user_plant_to_add)
    db.commit()
    db.refresh(user_plant_to_add)


def update_plant(db: Session, login: str, title: str, plant: schemas.PlantUpdate):
    plant_model = db.query(models.Plant).join(models.UserPlant, models.Plant.id == models.UserPlant.plant_id).\
        join(models.User, models.User.id == models.UserPlant.user_id).\
        where(and_(models.User.login == login, models.Plant.title == title)).first()

    plant_model.title = plant.title
    plant_model.description = plant.description
    plant_model.image = plant.image
    plant_model.privacy = plant.privacy

    db.add(plant_model)
    db.commit()
    db.refresh(plant_model)
    return plant_model


def delete_plant(db: Session, _id: int):
    db.query(models.UserPlant).filter(models.UserPlant.plant_id == _id).delete()
    db.query(models.Plant).filter(models.Plant.id == _id).delete()

    db.commit()
    return {f"Plant with id: {_id} has been successfully deleted!"}


def create_watering(db: Session, login: str, title: str, watering: schemas.WateringCreate):
    # Create watering calendar
    plant_model = get_alike_plants(db=db, user_login=login, plant_title=title).first()

    watering_model = models.Watering(
        week_day=watering.week_day,
        time=watering.time,
        last_watering=watering.last_watering
    )

    db.add(watering_model)
    db.commit()
    db.refresh(watering_model)

    add_plant_watering_row(db=db, plant_id=plant_model.id, watering_id=watering_model.id)
    return watering_model


def add_plant_watering_row(watering_id: int, plant_id: int, db: Session):
    model = models.PlantWatering(
        plant_id=plant_id,
        watering_id=watering_id
    )

    db.add(model)
    db.commit()
    db.refresh(model)
