from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.shortcuts import render 
from django.contrib.auth.hashers import check_password
from .models import User
from .serializer import SignupSerializer, UserSerializer
from .token import CreateToken


class AccountViewSet(APIView):
    def get(self, request):
        user = User.objects.all().first()
        return render(request, "test.html")


class SignupViewSet(APIView):
    def post(self, request):
        serializer = SignupSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Create JWT
        user = User.objects.get(email = request.data["email"])
        response = CreateToken(user)
        return response


class LoginViewSet(APIView):

    # login > METHOD = "POST"
    def post(self, request):

        email = request.data["email"]
        password = request.data["password"]

        if email is None or password is None :
        # blank email or password
            return Response({
                "message" : "email / password required",   
            }, status = status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email = email)

        if user is None:
        # not registered email
            return Response({
                "message" : "check username",
            }, status = status.HTTP_404_NOT_FOUND)

        if not check_password(password, user.password):
        # wrong password
            return Response({
                "message":"wrong password",
            }, status = status.HTTP_400_BAD_REQUEST)
        response = CreateToken(user)
        # Create JWT
        # token = TokenObtainPairSerializer.get_token(user)
        # refresh_token = str(token)
        # access_token = str(token.access_token)
        # response = Response({
        #     "user" : UserSerializer(user).data,
        #     "message" : "login success",
        #     "jwt_token" : {
        #         "access_token" : access_token,
        #         "refresh_token" : refresh_token,
        #     },
        # }, status = status.HTTP_200_OK)
        
        return response
    
class LogoutViewSet(APIView):
    # logout > METHOD = "POST"
    """
    <로그아웃 로직>

    토큰을 블랙리스트 등록함으로써 유저 인증 토큰 차단.
    JWT의 경우 DB에서 인증을 관리하는 것이 아니므로,
    토큰 자체를 차단함으로써 로그아웃 구현. 
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token = RefreshToken(request.data["refresh_token"])
        token.blacklist() # JWT Blacklist 등록
        return Response({
            "message" : "logout success"
        }, status = status.HTTP_202_ACCEPTED)




# class RefreshViewSet(APIView):
#     def post(self, request):
#         refresh_token = request.COOKIES.get('refreshtoken')
        
#         if refresh_token is None:
#             return Response({
#                 "message": "Authentication credentials were not provided."
#             }, status=status.HTTP_403_FORBIDDEN)
        
#         try:
#             payload = jwt.decode(
#                 refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256']
#             )

#         except:
#             return Response({
#                 "message": "expired refresh token, please login again."
#             }, status=status.HTTP_403_FORBIDDEN)
        
#         user = User.objects.filter(id=payload['user_id']).first()
        
#         if user is None:
#             return Response({
#                 "message": "user not found"
#             }, status=status.HTTP_400_BAD_REQUEST)
#         if not user.is_active:
#             return Response({
#                 "message": "user is inactive"
#             }, status=status.HTTP_400_BAD_REQUEST)
        
#         # access_token = generate_access_token(user)
        
#         return Response(status=status.HTTP_200_OK)
        
        
# class SigninViewSet(APIView):
#     def post(self, request):
