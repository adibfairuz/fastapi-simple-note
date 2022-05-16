from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT, POSTGRES_HOST

database_url = "postgresql://"+POSTGRES_USER+":"+POSTGRES_PASSWORD+"@"+POSTGRES_HOST+":"+POSTGRES_PORT+"/"+POSTGRES_DB

engine=create_engine(database_url, echo=True)


Base=declarative_base()

SessionLocal=sessionmaker(bind=engine)