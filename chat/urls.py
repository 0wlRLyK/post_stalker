from django.urls import path, re_path

from .views import ThreadView, InboxView, ChatView

app_name = 'chat'
urlpatterns = [
    path("", InboxView.as_view()),
    re_path(r"^d/(?P<username>[\w.@+-]+)/", ThreadView.as_view()),
    path("chat/<slug:slug>/", ChatView.as_view(), name="chat"),
]
