import uvicorn
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError, HTTPException
from app.helpers.response_helper import error
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routes import auth, posts, users

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    errors = list(map(lambda x: x["msg"], exc.errors()))
    return error(status.HTTP_400_BAD_REQUEST, 'Invalid request', errors)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return error(exc.status_code, exc.detail)

@app.exception_handler(Exception)
async def http_exception_handler():
    return error(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Internal server error')

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(users.router, prefix="/users", tags=["users"])

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8080, reload=True)