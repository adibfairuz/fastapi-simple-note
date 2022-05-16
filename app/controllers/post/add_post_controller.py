from app.helpers.response_helper import success
from app.services.post_service import PostService

class AddPostController:
    def __init__(self, payload, user_id: str):
        self.payload = payload
        self.user_id = user_id
    
    def __call__(self):
        post_service = PostService()
        post = post_service.create_post(self.payload, self.user_id)
        return success(post, status_code=201, message="Create post success")