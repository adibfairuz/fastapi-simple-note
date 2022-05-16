from pydantic import BaseModel, Field, EmailStr

class PostSchema(BaseModel):
    title: str
    body: str = Field(default=None)

class UserSchema(BaseModel):
    id: str = Field(default=None)
    fullname: str
    email: EmailStr
    password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str