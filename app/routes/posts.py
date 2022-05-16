from fastapi import APIRouter, Body, Depends
from app.helpers.jwt_helper import get_current_user
from app.models import schemas
from app.controllers.post import add_post_controller, get_post_controller, get_posts_controller, update_post_controller, delete_post_controller

router = APIRouter()

@router.post("/")
def create_post(post: schemas.PostSchema = Body(default=None), user = Depends(get_current_user)):
    post = add_post_controller.AddPostController(post, user['id'])
    return post()

@router.get("/")
def get_posts(user = Depends(get_current_user)):
    posts = get_posts_controller.GetPostsController(user['id'])
    return posts()

@router.get("/{id}")
def get_post_by_id(id: str, user = Depends(get_current_user)):
    post = get_post_controller.GetPostController(id, user['id'])
    return post()

@router.put("/{id}")
def update_post(id: str, post: schemas.PostSchema = Body(default=None), user = Depends(get_current_user)):
    updated_post = update_post_controller.UpdatePostController(id, user['id'], post)
    return updated_post()

@router.delete("/{id}")
def delete_post(id: str, user = Depends(get_current_user)):
    updated_post = delete_post_controller.DeletePostController(id, user['id'])
    return updated_post()