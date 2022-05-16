from app.helpers.response_helper import success
from app.models.schemas import PostSchema
from app.services.post_service import PostService

class UpdatePostController:
    def __init__(self, id: str, user_id: str, post: PostSchema):
        self.id = id
        self.user_id = user_id
        self.post = post
    
    def __call__(self):
        post_service = PostService()
        post = post_service.update_post(self.id, self.user_id, self.post)
        return success(post, status_code=200, message="Update post success")