from .models import OnlineUserActivity


class OnlineNowMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if not user.is_authenticated:
            return

        OnlineUserActivity.update_user_activity(user)
        response = self.get_response(request)
        return response
