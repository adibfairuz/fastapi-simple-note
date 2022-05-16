from app.db.database import Base
from sqlalchemy import ForeignKey, String, Column,Text
from sqlalchemy.orm import relationship


class UserTable(Base):
    __tablename__='user'
    id=Column(String,primary_key=True, unique=True)
    fullname=Column(String(200),nullable=False)
    email=Column(String(200),nullable=False,unique=True)
    password=Column(String(200),nullable=False)
    children=relationship('PostTable')

class PostTable(Base):
    __tablename__='post'
    id=Column(String,primary_key=True, unique=True, nullable=False)
    user_id=Column(String,ForeignKey('user.id'),nullable=False)
    title=Column(String(200),nullable=False)
    body=Column(Text,nullable=False)