from django.urls import path
from . import views

app_name = "mypage"

urlpatterns = [
    path('<int:user_id>/', views.MypageMainViewSet.as_view()),
    path('<int:user_id>/modify-info/',
         views.ModifyUserInformationViewSet.as_view()),
    path('myboardslists/', views.MyBoardsListViewSet.as_view()),
    path('change-password/', views.ChangePasswordViewSet.as_view()),
]
