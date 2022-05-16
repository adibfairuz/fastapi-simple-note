import time
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.config.settings import JWT_ALGORITHM, JWT_SECRET

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def signJWT(payload, exp = 3600):
    payload = dict(payload)
    payload["exp"] = time.time() + exp
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decodeJWT(token: str):
    decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    if decode_token['exp'] >= time.time():
        return decode_token
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired!")

async def get_decoded_data(token: str = Depends(oauth2_scheme)):
    try:
        data = decodeJWT(token)
        return data
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token!")

def check_token_type(data, type):
    try:
        invalidate_token = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token!")
        if(data['type'] == type):
            return data
        raise invalidate_token
    except Exception as e:
        raise invalidate_token

async def get_current_user(data = Depends(get_decoded_data)):
    return check_token_type(data, 'access_token')

async def get_refresh_data(data = Depends(get_decoded_data)):
    return check_token_type(data, 'refresh_token')