from django.urls import path
from . import views


app_name = "main"

urlpatterns = [
    path('', views.MainViewSet.as_view(), name="main"),  # 게시판
]
