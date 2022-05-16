import uvicorn
from fastapi import FastAPI, Body, Depends, status
from fastapi.exceptions import RequestValidationError, HTTPException
from app.helpers.jwt_helper import get_current_user, get_refresh_data
from app.helpers.response_helper import error
from app.models import schemas
from app.controllers.user import get_user_controller
from app.controllers.auth import login_controller, signup_controller, refresh_token_controller, logout_controller
from app.controllers.post import add_post_controller, get_post_controller, get_posts_controller, update_post_controller, delete_post_controller
from starlette.exceptions import HTTPException as StarletteHTTPException

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

@app.get("/", tags=["test"])
def greet():
    return {"message": "Hello World"}

@app.get("/user", tags=["user"])
def user(user = Depends(get_current_user)):
    user = get_user_controller.GetUserController(user)
    return user()

@app.post("/auth/signup", tags=["auth"])
def signup(user : schemas.UserSchema = Body(default=None)):
    signup = signup_controller.SignupController(user)
    return signup()

@app.post("/auth/login", tags=["auth"])
def login(user: schemas.UserLoginSchema = Body(default=None)):
    login = login_controller.LoginController(user)
    return login()

@app.delete("/auth/logout", tags=["auth"])
def logout(data = Depends(get_refresh_data)):
    refresh_token_id = data['refresh_token_id']
    logout = logout_controller.LogoutController(refresh_token_id)
    return logout()

@app.post("/auth/refresh-token", tags=["auth"])
def refresh_token(data = Depends(get_refresh_data)):
    refresh_token_id = data['refresh_token_id']
    refresh_token = refresh_token_controller.RefreshTokenController(refresh_token_id)
    return refresh_token()

@app.post("/posts", tags=["posts"])
def create_post(post: schemas.PostSchema = Body(default=None), user = Depends(get_current_user)):
    post = add_post_controller.AddPostController(post, user['id'])
    return post()

@app.get("/posts", tags=["posts"])
def get_posts(user = Depends(get_current_user)):
    posts = get_posts_controller.GetPostsController(user['id'])
    return posts()

@app.get("/posts/{id}", tags=["posts"])
def get_post_by_id(id: str, user = Depends(get_current_user)):
    post = get_post_controller.GetPostController(id, user['id'])
    return post()

@app.put("/posts/{id}", tags=["posts"])
def update_post(id: str, post: schemas.PostSchema = Body(default=None), user = Depends(get_current_user)):
    updated_post = update_post_controller.UpdatePostController(id, user['id'], post)
    return updated_post()

@app.delete("/posts/{id}", tags=["posts"])
def delete_post(id: str, user = Depends(get_current_user)):
    updated_post = delete_post_controller.DeletePostController(id, user['id'])
    return updated_post()

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8080, reload=True)