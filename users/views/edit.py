from django.views.generic import UpdateView
from django.views.generic import UpdateView

from users.models import User
from utils.views.mixins import JsonableResponseMixin


class CurrentUserMixin(object):
    model = User

    def get_object(self, *args, **kwargs):
        try:
            obj = super(CurrentUserMixin, self).get_object(*args, **kwargs)
        except AttributeError:
            # SingleObjectMixin throws an AttributeError when no pk or slug
            # is present on the url. In those cases, we use the current user
            obj = self.request.user

        return obj


class UserEdit(CurrentUserMixin, JsonableResponseMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "birthday", "gender", "country", "state", "signature"]
    template_name = "users/edit/user_form.html"
    success_url = "/"

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.get_form()
        print(request.POST.get("signature"), request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            for key, value in form.cleaned_data.items():
                if getattr(user, key) != value:
                    print(key, value)
                    setattr(user, key, value)
                # if key == "signature":
                #
                #     signature = bleach.clean(request.POST.get("signature"))
                #     setattr(user, key, signature)
                #     print(signature)
            user.save()
            return JsonResponse({"result": True})
        return self.form_invalid(form=form, request=request)
