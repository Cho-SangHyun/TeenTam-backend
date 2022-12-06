from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from boards.models import Boards, BoardCategories
from account.serializer import UserMainSerializer
from boards.serializer import BoardsListSerializer
from rest_framework import status
from rest_framework.response import Response
# Create your views here.


class MainViewSet(APIView):
    
    def get(self, request):
        
        user_id = request.GET.get("user_id")
        category_list_name = request.GET.get("category_list").split(",")
        boards = Boards.objects.none()
        for category_name in category_list_name:
            category_id = BoardCategories.objects.filter(name=category_name).first().id
            boards |= Boards.objects.filter(boards_category_id=category_id)[:5]
            
        user = User.objects.get(id=user_id)
        user_serializer = UserMainSerializer(user)
        board_serializer = BoardsListSerializer(boards, many=True)
        
        response = Response({
            "user_data" : user_serializer.data,
            "boards_data" : board_serializer.data
            }, status=status.HTTP_200_OK)
        return response
    