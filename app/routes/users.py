from fastapi import APIRouter, Body, Depends
from app.helpers.jwt_helper import get_current_user
from app.controllers.user import get_user_controller

router = APIRouter()

@router.get("/me")
def user(user = Depends(get_current_user)):
    user = get_user_controller.GetUserController(user)
    return user()