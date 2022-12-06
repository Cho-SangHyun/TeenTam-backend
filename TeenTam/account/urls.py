from django.urls import path
from .views import account_find_views, authenticate_views, account_validation_views

app_name = "account"

urlpatterns = [
    path('login/', authenticate_views.LoginViewSet.as_view(), name="login"),
    path('logout/', authenticate_views.LogoutViewSet.as_view(), name="logout"),
    path('signup/', authenticate_views.SignupViewSet.as_view(), name="signup"),
    path('find-email/', account_find_views.FindEmailViewSet.as_view(), name="find-email"),
    path('find-password/', account_find_views.FindPasswordViewSet.as_view(), name="find-password"),
    path('username-validate/', account_validation_views.UsernameValidateViewSet.as_view(),
         name="username-validate")
]
