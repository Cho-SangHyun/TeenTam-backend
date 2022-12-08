from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from account.models import User
from account.serializer import ProfileImageSerializer

class UploadProfileImage(APIView):
    
    def post(self, request):

        user_id = request.POST["user_id"]
        img = request.FILES["profile_image"]
        user = User.objects.filter(id=user_id).first()
        
        user.profile_image = img
        user.save()
        
        response = Response({
            "message" : "profile_image uploaded successfullyJ"
        },status=status.HTTP_201_CREATED)
        return response
    
class GetProfileImage(APIView):
    
    def get(self, request):
        
        user_id = request.GET.get("user_id")
        profile_image = User.objects.only("profile_image").filter(id=user_id).first()
        serializer = ProfileImageSerializer(profile_image)
        data = serializer.data
        
        response = Response({
            "message" : "profile_image url",
            "data" : data
        }, status=status.HTTP_200_OK)
        
        return response
        