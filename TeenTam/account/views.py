from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .serializer import UserSerializer
from django.conf import settings
from django.shortcuts import render 
from django.contrib.auth.hashers import check_password
from . import token, authenticate
import jwt


class AccountViewSet(APIView):
    def get(self, request):
        user = User.objects.all().first()
        tok = token.CreateToken(user)
        print(tok)
        return render(request, "test.html")

class LoginViewSet(APIView):
    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        if email is None or password is None :
        # blanck email or password
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


        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        response = Response({
            "user" : UserSerializer(user).data,
            "message" : "login success",
            "jwt_token" : {
                "access_token" : access_token,
                "refresh_token" : refresh_token,
            },
        }, status = status.HTTP_200_OK)
        
        return response



class RefreshViewSet(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshtoken')
        
        if refresh_token is None:
            return Response({
                "message": "Authentication credentials were not provided."
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            payload = jwt.decode(
                refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256']
            )

        except:
            return Response({
                "message": "expired refresh token, please login again."
            }, status=status.HTTP_403_FORBIDDEN)
        
        user = User.objects.filter(id=payload['user_id']).first()
        
        if user is None:
            return Response({
                "message": "user not found"
            }, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({
                "message": "user is inactive"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # access_token = generate_access_token(user)
        
        return Response(status=status.HTTP_200_OK)
        
        
# class SigninViewSet(APIView):
#     def post(self, request):
