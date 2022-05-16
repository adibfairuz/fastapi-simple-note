from app.helpers.response_helper import success

class GetUserController:
    def __init__(self, user):
        self.user = user
    def __call__(self):
        payload = {
            'id': self.user['id'],
            'fullname': self.user['fullname'],
            'email': self.user['email'],
        }
        return success(payload, status_code=200, message="Get user success")