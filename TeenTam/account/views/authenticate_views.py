from rest_framework.views import APIView
from ..serializer import SignupSerializer, LoginSerializer
from ..models import User
from ..token import CreateToken, BlacklistToken
from rest_framework import permissions

# 로그인
class LoginViewSet(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=request.data["email"])
        response = CreateToken(user)

        return response

# 로그아웃
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

# 회원가입
class SignupViewSet(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=request.data["email"])
        response = CreateToken(user)

        return response


# 로그인
class LoginViewSet(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=request.data["email"])
        response = CreateToken(user)

        return response

# 로그아웃
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