from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from .models import User
from .serializer import FindEmailSerializer, FindPasswordSerializer, LoginSerializer, SignupSerializer, UsernameSerializer
from .token import BlacklistToken, CreateToken
from .authenticate import GMailClient, TemporaryPassword
from django.contrib.auth.hashers import make_password


class SignupViewSet(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=request.data["email"])
        response = CreateToken(user)

        return response


class UsernameValidateViewSet(APIView):

    def post(self, request):
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = Response({
            "message": "you can use this username"
        }, status=status.HTTP_202_ACCEPTED)
        return response


class LoginViewSet(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=request.data["email"])
        response = CreateToken(user)

        return response


class LogoutViewSet(APIView):
    """
    <로그아웃 로직>

    토큰을 블랙리스트 등록함으로써 유저 인증 토큰 차단.
    JWT의 경우 DB에서 인증을 관리하는 것이 아니므로,
    토큰 자체를 차단함으로써 로그아웃 구현.
    """
    permission_classes = [permissions.IsAuthenticated]  # 인증된 유저만 접근 가능

    def post(self, request):

        response = BlacklistToken(request)
        return response


class FindEmailViewSet(APIView):

    def post(self, request):

        serializer = FindEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ph_num = request.data["phone_number"]
        user_email = User.objects.get(phone_number=ph_num).only("email")
        response = Response({
            "message": "email find success",
            "email": user_email,
        }, status=status.HTTP_200_OK)

        return response


class FindPasswordViewSet(APIView):

    def post(self, request):

        serializer = FindPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data["email"]
        user = User.objects.get(email=email)

        # 임시 비밀번호 전송
        temp_password = TemporaryPassword()
        subject = f"from.TeenTam, {user.username}님, 임시 비밀번호 입니다."
        content = f"{user.username}님의 임시 비밀번호는 [{temp_password}] 입니다."

        email_username = "kccce6567@gmail.com"
        email_password = "hlxwkcichwvnxcmz"
        sendmail = GMailClient(email_username, email_password)
        sendmail.send_email(email, subject, content)

        new_password = make_password(temp_password)
        user.password = new_password
        user.save()

        response = Response({
            "message": "new password issued, check the email"
        }, status=status.HTTP_200_OK)

        return response
