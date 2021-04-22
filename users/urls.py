from django.urls import path

from users import views as u_views

app_name = "users"
urlpatterns = [
    path("rep/<int:pk>/", u_views.ReputationDetailView.as_view(), name="user_reputation"),
    path("add/rep/<int:user_id>/", u_views.ReputationCreateView.as_view(), name="user_reputation_add"),
    path("money/<int:pk>/", u_views.TransactionDetailView.as_view(), name="user_money"),
    path("transfer/money/<int:user_id>/", u_views.TransactionCreateView.as_view(), name="user_money_transfer"),

]
