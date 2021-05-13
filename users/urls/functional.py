from django.urls import path

from users.views import funcs, equip

app_name = "users"
urlpatterns = [
    path("rep/<int:pk>/", funcs.ReputationDetailView.as_view(), name="user_reputation"),
    path("add/rep/<int:user_id>/", funcs.ReputationCreateView.as_view(), name="user_reputation_add"),

    path("money/<int:pk>/", funcs.TransactionDetailView.as_view(), name="user_money"),
    path("transfer/money/<int:user_id>/", funcs.TransactionCreateView.as_view(), name="user_money_transfer"),

    path("awards/<int:pk>/", funcs.AwardDetailView.as_view(), name="user_awards"),
    path("add/award/<int:user_id>/", funcs.AwardAddView.as_view(), name="user_award_add"),

    path("img_select/", funcs.SelectChatImageView.as_view(), name="img_select"),
    path("status_set/", funcs.ChangeStatusView.as_view(), name="set_status"),
    path("change_username/", funcs.ChangeUsername.as_view(), name="change_username"),

    path("shop/", equip.EquipmentShop.as_view(), name="equip_shop"),

]
