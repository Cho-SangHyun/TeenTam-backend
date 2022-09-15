from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
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

        username = request.GET.get["username"]
        password = request.GET.get["password"]
        # blanck username or password
        if username is None or password is None :
            return Response({
                "message" : "username / password required",   
            }, status = status.HTTP_400_BAD_REQUEST)
        # not registered username
        user = User.objects.get(username = username)
        if user is None:
            return Response({
                "message" : "check username",
            }, status = status.HTTP_404_NOT_FOUND)
        # wrong password
        if not check_password(password, user.password):
            return Response({
                "message":"wrong password",
            }, status = status.HTTP_400_BAD_REQUEST)

        response = Response(status=status.HTTP_200_OK)  
        return authenticate.jwt_login(response, user)



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
        
        access_token = generate_access_token(user)
        
        return Response(
            {
                'access_token': access_token,
            }
        )
        
        