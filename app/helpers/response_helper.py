from fastapi import HTTPException
from fastapi.responses import JSONResponse

def success(payload, status_code, message, messages=[]):
    response = JSONResponse(
        status_code=status_code,
        content={
            'payload': payload,
            'status_code': status_code,
            'message': message,
            'messages': messages,
            'ok': True
        }
    )
    return response
    
def error(status_code, message, messages=[]):
    response = JSONResponse(
        status_code=status_code,
        content={
            'payload': None,
            'status_code': status_code,
            'message': message,
            'messages': messages,
            'ok': False
        }
    )
    return response