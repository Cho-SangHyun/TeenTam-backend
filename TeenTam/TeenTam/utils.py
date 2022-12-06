from rest_framework.response import Response
from rest_framework import status

def BadRequest(message):
    response = Response({
        "message" : message
    }, status=status.HTTP_400_BAD_REQUEST)
    return response