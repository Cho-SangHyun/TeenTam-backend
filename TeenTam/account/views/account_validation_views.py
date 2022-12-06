from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializer import UsernameSerializer
from rest_framework import status

# 닉네임 유효성 검사
class UsernameValidateViewSet(APIView):

    def post(self, request):    
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = Response({
            "message": "you can use this username"
        }, status=status.HTTP_202_ACCEPTED)
        return response