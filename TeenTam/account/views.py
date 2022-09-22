from rest_framework import permissions
from rest_framework.views import APIView
from django.shortcuts import render 
from .models import User
from .serializer import LoginSerializer, SignupSerializer
from .token import BlacklistToken, CreateToken


class AccountViewSet(APIView):
    
    def get(self, request):
        user = User.objects.all().first()

        return render(request, "test.html")


class SignupViewSet(APIView):

    def post(self, request):
        serializer = SignupSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email = request.data["email"])
        response = CreateToken(user)

        return response


class LoginViewSet(APIView):

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email = request.data["email"])
        response = CreateToken(user)

        return response
    

class LogoutViewSet(APIView):
    """
    <로그아웃 로직>

    토큰을 블랙리스트 등록함으로써 유저 인증 토큰 차단.
    JWT의 경우 DB에서 인증을 관리하는 것이 아니므로,
    토큰 자체를 차단함으로써 로그아웃 구현.
    """
    permission_classes = [permissions.IsAuthenticated] # 인증된 유저만 접근 가능

    def post(self, request):
        
        response = BlacklistToken(request)
        return response