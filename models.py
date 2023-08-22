from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    login = Column(String, unique=True)
    password = Column(String)

    plants = relationship("Plant", back_populates="user")

class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    image = Column(String)
    privacy = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="plants")



