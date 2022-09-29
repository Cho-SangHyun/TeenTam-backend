from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Boards
from .serializer import CreateBoardSerializer, CreateBoardCategorySerializer, BoardDetailSerializer
# Create your views here.


class BoardListViewSet(APIView):

    def get(self, request):
        return request


class BoardDetailViewSet(APIView):
    
    def get(self, request, boards_id):
        
        board = Boards.objects.get(id = boards_id)
        
        if board is None:
            response = Response({
                "message" : "wrong board id"
            }, status = status.HTTP_404_NOT_FOUND)
            return response
        
        serializer = BoardDetailSerializer(board)
        print(serializer.data)
        serializer.is_valid()
        data = serializer.data
        
        response = Response({     
            "data" : data
        }, status = status.HTTP_200_OK)
        return response
    
    
class CreateBoardViewSet(APIView):
    
    def post(self, request):
        
        serializer = CreateBoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        
        response = Response({
            "message" : "create board successfully"
            
        }, status = status.HTTP_201_CREATED)
        
        return response
    
class TestBoardViewSet(APIView):
    
    def get(self, request):
        
        data = Boards.objects.all()
        
        response = Response({
            "data" : data
        }, status = status.HTTP_200_OK)
        
        return response
    
class CreateBoardCategoryViewSet(APIView):
    
    def post(self, request):
        
        serializer = CreateBoardCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
        response = Response({
            "message" : "create board category successfully"
        }, status = status.HTTP_201_CREATED)
        return response