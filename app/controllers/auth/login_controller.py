from app.helpers.response_helper import success
from app.services.auth_service import AuthService

class LoginController:
    def __init__(self, payload):
        self.payload = payload
    
    def __call__(self):
        auth_service = AuthService()
        response = auth_service.login(self.payload)
        return success(response, status_code=200, message="Login success")