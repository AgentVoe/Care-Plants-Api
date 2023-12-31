from typing import Annotated
import uvicorn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


import crud
import models
import schemas
from database import SessionLocal, engine


from utils import check_password, hash_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/{user_login}", response_model=list[schemas.UsersSchema])
def get_plants(user_login: str, db: Session = Depends(get_db)):
    plants = crud.get_user_plants(db, user_login)
    if plants is None:
        raise HTTPException(status_code=400, detail='No plants found!')
    else:
        return plants


@app.get("/users/{user_login}/plants", response_model=list[schemas.PlantSchema])
def find_alike_plants(user_login: str, plant_title: str, db: Session = Depends(get_db)):
    plants = crud.get_alike_plants(db, user_login, plant_title)
    if plants is None:
        raise HTTPException(status_code=400, detail='No plants found!')
    else:
        return plants


@app.post("/users/{login}/plants/", response_model=schemas.PlantCreate)
def create_plant(login: str, plant: schemas.PlantCreate, db: Session = Depends(get_db)):
    _plant = crud.get_alike_plants(user_login=login, db=db, plant_title=plant.title).first()
    if _plant is None:
        return crud.create_plant(plant=plant, db=db, login=login)
    else:
        raise HTTPException(status_code=400, detail='Plant already exists!')


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_login(db, user.login)
    if db_user is None:
        return crud.create_user(db=db, user=user)
    else:
        raise HTTPException(status_code=400, detail='Login already exists!')


@app.post("/users/{login}/{plant_title}/watering/", response_model=schemas.WateringCreate)
def create_watering(login: str, plant_title: str, watering: schemas.WateringCreate, db: Session = Depends(get_db)):
    watering_model = crud.create_watering(db=db, login=login, title=plant_title, watering=watering)
    if watering_model is None:
        raise HTTPException(status_code=400, detail='Something went wrong!')
    return watering_model


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User mot found!")
    return db_user


# Don't sure how this must work, solve it later
@app.put("/users/{login}/{plant_title}/", response_model=schemas.PlantUpdate)
def update_plant(login: str, plant_title: str, plant: schemas.PlantUpdate, db: Session = Depends(get_db)):
    plant_model = crud.get_alike_plants(db=db, user_login=login, plant_title=plant_title)
    if plant_model is None:
        raise HTTPException(status_code=404, detail='Something went wrong!')
    
    return crud.update_plant(db=db, login=login, title=plant_title, plant=plant)


@app.delete("/users/{login}/{plant_title}/")
def delete_plant(login: str, plant_title: str, db: Session = Depends(get_db)):
    plant_model = crud.get_alike_plants(db=db, user_login=login, plant_title=plant_title).first()
    if plant_model is None:
        raise HTTPException(status_code=404, detail='Something went wrong!')
    return crud.delete_plant(db=db, _id=plant_model.id)


@app.get("/community/plants/", response_model=list[schemas.PlantSchema])
def get_public_plants(db: Session = Depends(get_db)):
    return crud.get_all_public_plants(db=db)


@app.post("/community/plants/{login}/{plant_title}/")
def add_public_plant(plant_title: str, login: str, db: Session = Depends(get_db)):
    return crud.add_public_plant(title=plant_title, login=login, db=db)


@app.post("/login/")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user_model = crud.get_user_by_login(login=form_data.username, db=db)
    print(form_data.password.encode('utf-8'), user_model.password)
    if check_password(form_data.password.encode('utf-8'), user_model.password):
        return {"access_token": user_model.login, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
