from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


def CreateToken(user):

    token = TokenObtainPairSerializer.get_token(user)  # Create JWT
    refresh_token = str(token)
    access_token = str(token.access_token)
    response = Response({
        "user": UserSerializer(user).data,
        "message": "login success",
        "jwt_token": {
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
    }, status=status.HTTP_200_OK)
    return response


def BlacklistToken(request):

    token = RefreshToken(request.data["refresh_token"])
    token.blacklist()  # JWT Blacklist 등록
    response = Response({
        "message": "logout success"
    }, status=status.HTTP_202_ACCEPTED)
    return response
