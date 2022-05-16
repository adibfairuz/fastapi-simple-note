import json
from uuid import uuid4
from app.helpers.response_helper import success
from app.models import schemas
from app.db.database import SessionLocal
from app.models.tables import PostTable
from fastapi import HTTPException, status
from sqlalchemy.ext.serializer import loads, dumps

db = SessionLocal()

class PostService:
    def get_post(self, id: str, user_id: str):
        db_post = db.query(PostTable).filter(PostTable.id == id).one_or_none()
        if db_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if db_post.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to access this resource")
        else:
            payload = {
                'id': db_post.id,
                'title': db_post.title,
                'body': db_post.body
            }
            return payload

    def get_posts(self, user_id: str):
        db_posts = []
        for u in db.query(PostTable).filter(PostTable.user_id == user_id).all():
            db_posts.append({
                'id': u.id,
                'title': u.title,
                'body': u.body,
            })
        if len(db_posts) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts are empty")
        else:
            payload = db_posts
            return payload

    def create_post(self, post: schemas.PostSchema, user_id: str):
        new_post = PostTable(
            id=str(uuid4()),
            user_id=user_id,
            title=post.title,
            body=post.body,
        )
        db.add(new_post)
        db.commit()
        payload = {
            'id': new_post.id,
            'title': new_post.title,
            'body': new_post.body,
        }
        return payload


    def update_post(self, id: str, user_id: str, post: schemas.PostSchema):
        db_post = db.query(PostTable).filter(PostTable.id == id).one_or_none()
        if db_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if db_post.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this resource")
        else:
            update_post = PostTable(
                title=post.title,
                body=post.body,
            )
            payload = {
                'title': update_post.title,
                'body': update_post.body,
            }
            db.query(PostTable).filter(PostTable.id == id).update(payload)
            return payload

    def delete_post(self, id: str, user_id: str):
        try:
            db_post = db.query(PostTable).filter(PostTable.id == id).one_or_none()
            if db_post is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
            if db_post.user_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to access this resource")
            else:
                db.query(PostTable).filter(PostTable.id == id).delete()
                payload = {
                    'id': db_post.id,
                    'title': db_post.title,
                }
                return payload
        except HTTPException as e:
            raise HTTPException(e.status_code, e.detail)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    