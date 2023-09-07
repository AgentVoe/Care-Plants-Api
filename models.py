from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base



# Many-to-many table to connect Plants and Watering
plant_watering = Table('plant_watering', Base.metadata,
                       Column('id', Integer, primary_key=True, index=True, autoincrement=True),
                       Column('plant_id', ForeignKey('plants.id'), primary_key=True),
                       Column('watering_id', ForeignKey('watering.id'), primary_key=True)
                       )

# User, Plant, Watering classes representing tables structure in database


class UserPlant(Base):
    __tablename__ = 'user_plant'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    plant_id = Column(Integer, ForeignKey('plants.id'), primary_key=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    login = Column(String, unique=True)
    password = Column(String)

    plants = relationship("Plant", secondary='user_plant', back_populates="users")


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    image = Column(String)
    privacy = Column(Boolean, default=True)

    users = relationship("User",  secondary='user_plant',  back_populates="plants")

    waterings = relationship("Watering", secondary="plant_watering", back_populates='plants')


class Watering(Base):
    __tablename__ = 'watering'

    id = Column(Integer, primary_key=True, index=True)
    week_day = Column(Integer)
    time = Column(DateTime)
    last_watering = Column(DateTime)

    plants = relationship("Plant", secondary='plant_watering', back_populates='waterings')

