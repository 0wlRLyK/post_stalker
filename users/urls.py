from django.urls import path

from users import views as u_views

app_name = "users"
urlpatterns = [
    path("rep/<int:pk>/", u_views.ReputationDetailView.as_view(), name="user_reputation"),
    path("add/rep/<int:user_id>/", u_views.ReputationCreateView.as_view(), name="user_reputation_add"),

    path("money/<int:pk>/", u_views.TransactionDetailView.as_view(), name="user_money"),
    path("transfer/money/<int:user_id>/", u_views.TransactionCreateView.as_view(), name="user_money_transfer"),

    path("awards/<int:pk>/", u_views.AwardDetailView.as_view(), name="user_awards"),
    path("add/award/<int:user_id>/", u_views.AwardAddView.as_view(), name="user_award_add"),

    path("img_select/", u_views.SelectChatImageView.as_view(), name="img_select"),
    path("status_set/", u_views.ChangeStatusView.as_view(), name="set_status"),
    path("change_username/", u_views.ChangeUsername.as_view(), name="change_username"),

]
