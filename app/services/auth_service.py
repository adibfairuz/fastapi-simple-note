import json
import time
from app.helpers.response_helper import error, success
from app.models.schemas import UserLoginSchema, UserSchema
from app.helpers.jwt_helper import signJWT
from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from app.models.tables import UserTable
from app.db.database import SessionLocal
from fastapi import HTTPException, status
from app.helpers.redis_helper import redis

db = SessionLocal()

class AuthService:
    def get_user(self, user):
        db_user = db.query(UserTable).filter(UserTable.email == user.email).one_or_none()
        if db_user is None:
            return None
        else:
            return db_user

    def signup(self, user: UserSchema):
        try:
            db_user = self.get_user(user)
            if db_user is None:
                new_user = UserTable(
                    id=str(uuid4()),
                    fullname=user.fullname,
                    email=user.email,
                    password=user.password
                )
                db.add(new_user)
                db.commit()
                payload = {
                    'id': new_user.id,
                    'fullname': new_user.fullname,
                    'email': new_user.email
                }
                return payload
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')

    def login(self, user: UserLoginSchema):
        try:
            user_data = self.get_user(user)
            if user_data is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            else:
                if user_data.email == user.email and user_data.password == user.password:
                    access_token = {
                        'id': user_data.id,
                        'fullname': user_data.fullname,
                        'email': user_data.email,
                        'type': 'access_token'
                    }
                    refresh_token = dict(access_token)
                    refresh_token['refresh_token_id'] = str(uuid4())
                    refresh_token['type'] = 'refresh_token'
                    payload = {
                        "access_token": signJWT(access_token),
                        "refresh_token": signJWT(refresh_token, 86400),
                    }
                    redis.set(refresh_token['refresh_token_id'], json.dumps(access_token), 86400)
                    return payload
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login invalid")
                
        except HTTPException as e:
            raise HTTPException(e.status_code, e.detail)
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal server error')

    def refresh_token(self, refresh_token_id: str):
        try:
            data = redis.get(refresh_token_id)
            if data is not None:
                access_token = json.loads(data)
                payload = {
                    'access_token': signJWT(access_token),
                }
                return payload
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token invalid")
        except HTTPException as e:
            raise HTTPException(e.status_code, e.detail)
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal server error')
    
    def logout(self, refresh_token_id: str):
        try:
            data = redis.get(refresh_token_id)
            if data is not None:
                redis.delete(refresh_token_id)
                return None
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token invalid")
        except HTTPException as e:
            raise HTTPException(e.status_code, e.detail)
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal server error')
