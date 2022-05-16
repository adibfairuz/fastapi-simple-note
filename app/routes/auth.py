from fastapi import APIRouter, Body, Depends
from app.helpers.jwt_helper import get_refresh_data
from app.models import schemas
from app.controllers.auth import login_controller, signup_controller, refresh_token_controller, logout_controller

router = APIRouter()

@router.post("/signup")
def signup(user : schemas.UserSchema = Body(default=None)):
    signup = signup_controller.SignupController(user)
    return signup()

@router.post("/login")
def login(user: schemas.UserLoginSchema = Body(default=None)):
    login = login_controller.LoginController(user)
    return login()

@router.delete("/logout")
def logout(data = Depends(get_refresh_data)):
    refresh_token_id = data['refresh_token_id']
    logout = logout_controller.LogoutController(refresh_token_id)
    return logout()

@router.post("/refresh-token")
def refresh_token(data = Depends(get_refresh_data)):
    refresh_token_id = data['refresh_token_id']
    refresh_token = refresh_token_controller.RefreshTokenController(refresh_token_id)
    return refresh_token()