from .models import OnlineUserActivity


class OnlineNowMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        response = self.get_response(request)
        if user.is_authenticated:
            OnlineUserActivity.update_user_activity(user)
            return response
        else:
            return response
