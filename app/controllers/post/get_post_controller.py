from app.helpers.response_helper import success
from app.services.post_service import PostService

class GetPostController:
    def __init__(self, id: str, user_id: str):
        self.id = id
        self.user_id = user_id
    
    def __call__(self):
        post_service = PostService()
        post = post_service.get_post(self.id, self.user_id)
        return success(post, status_code=200, message="Get post success")