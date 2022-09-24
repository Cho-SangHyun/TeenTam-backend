from django.urls import path
from . import views


app_name = "boards"

urlpatterns = [
    path('<int:boards_ctg>/',views.BoardListViewSet.as_view(),name="boards_list"),
    # path('find-email', views.FindEmailViewSet.as_view(), name="find-email"),
    # path('find-password', views.FindPasswordViewSet.as_view(), name="find-password"),
]