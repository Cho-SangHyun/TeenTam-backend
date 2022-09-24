from django.urls import path
from . import views


app_name = "account"

urlpatterns = [
    path('',views.AccountViewSet.as_view(),name="account"),
    path('login/', views.LoginViewSet.as_view(), name="login"),
    path('logout/', views.LogoutViewSet.as_view(), name="logout"),
    path('signup/', views.SignupViewSet.as_view(), name="signup"),
    path('find-email/', views.FindEmailViewSet.as_view(), name="find-email"),
    path('find-password/', views.FindPasswordViewSet.as_view(), name="find-password"),
]