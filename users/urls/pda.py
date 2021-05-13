from django.urls import path
from userena import views as userena_views

from users.views import userena as my_userena
from users.views.edit import UserEdit
from users.views.userena import profile_detail as pda_detail
from users.views.userena import profile_detail_current_user

app_name = "pda"
urlpatterns = [
    path("", profile_detail_current_user, name="my_pda"),
    path("n/<username>/", userena_views.profile_detail, name="user_pda"),
    path("uid/<int:uid>/", pda_detail, name="user_pda_id"),
    path("signup/", userena_views.signup, name="userena_signup"),
    path("login/", userena_views.signin, name="userena_signin"),
    path("logout/", userena_views.SignoutView.as_view(), name="userena_signout"),
    path("edit/", UserEdit.as_view(), name="user_edit"),
    path("edit_email/",
         my_userena.email_change,
         name="user_email_change",
         ),
    path("email/complete/",
         my_userena.direct_to_user_template,
         {"template_name": "userena/email_change_complete.html"},
         name="userena_email_change_complete",
         ),
    path("change_password/",
         my_userena.password_change,
         name="user_password_change",
         ),
]
