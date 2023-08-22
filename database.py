from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Keys import user_name, password


SQL_ALCHEMY_DATABASE_URL = f"postgresql://{user_name}:{password}@localhost:5432/CarePlants"
engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
