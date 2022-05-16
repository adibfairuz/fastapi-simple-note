from app.helpers.response_helper import success
from app.services.post_service import PostService

class GetPostsController:
    def __init__(self, user_id: str):
        self.user_id = user_id
    
    def __call__(self):
        post_service = PostService()
        post = post_service.get_posts(self.user_id)
        return success(post, status_code=200, message="Get posts success")