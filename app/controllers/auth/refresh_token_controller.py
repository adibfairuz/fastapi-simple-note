from app.helpers.response_helper import success
from app.services.auth_service import AuthService

class RefreshTokenController:
    def __init__(self, refresh_token_id):
        self.refresh_token_id = refresh_token_id
    
    def __call__(self):
        auth_service = AuthService()
        response = auth_service.refresh_token(self.refresh_token_id)
        return success(response, status_code=200, message="Refresh token success")