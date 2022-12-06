from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..models import Boards, Likes
from ..serializer import *



# 게시글 좋아요 기능
class BoardsLikeViewSet(APIView):

    def post(self, request):

        boards_id = request.data["likes_board"]
        user_id = request.data["likes_user"]
        # 이미 좋아요 한 사용자 확인
        if Likes.objects.filter(likes_board=boards_id, likes_user=user_id).exists():
            response = Response({
                "message": "user already like this board"
            }, status=status.HTTP_200_OK)
            return response

        board = Boards.objects.get(id=boards_id)
        board.like += 1
        board.save()

        serializer = LikesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        response = Response({
            "message": "like success",
            "likes": board.like
        }, status=status.HTTP_200_OK)
        return response
