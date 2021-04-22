from django.urls import path

from users.views import ReputationDetailView, ReputationCreateView

app_name = "users"
urlpatterns = [
    path("rep/<int:pk>/", ReputationDetailView.as_view(), name="user_reputation"),
    path("add/rep/<int:user_id>/", ReputationCreateView.as_view(), name="user_reputation_add"),

]
