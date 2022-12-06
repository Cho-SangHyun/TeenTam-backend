from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializer import FindEmailSerializer, FindPasswordSerializer
from ..models import User
from .authenticate_utils_views import TemporaryPassword, GMailClient
from django.contrib.auth.hashers import make_password

# 이메일 찾기
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

# 비밀번호 찾기
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
