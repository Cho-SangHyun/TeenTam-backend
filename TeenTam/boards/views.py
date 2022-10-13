from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Boards, Likes
from .serializer import *


# 게시판별 게시글 목록 GET
class BoardListViewSet(APIView):

    def get(self, request, boards_category):

        page = int(request.GET.get('page'))
        offset = int(request.GET.get('offset'))
        order = request.GET.get('order')

        cursor = (page-1)*offset

        boards = Boards.objects.filter(
            boards_category=boards_category).order_by(order)
        sql = ('SELECT * FROM boards_boards AS boards WHERE boards.boards_category_id = ' +
               str(boards_category) + ' AND boards.delete_date IS NULL ORDER BY pub_date DESC LIMIT ' +
               str(offset) + ' OFFSET ' + str(cursor))

        boards = Boards.objects.raw(sql)
        boards_num = len(boards)  # 리스트 내 게시글 갯수
        serializer = BoardListSerializer(boards, many=True)

        data = serializer.data
        response = Response({
            "message": "GET boards list success",
            "data": data,
            "boards_num": boards_num,
        })

        return response


class BoardDetailViewSet(APIView):

    def get(self, request, boards_category, boards_id):

        board = Boards.objects.filter(id=boards_id)
        if board is None:
            response = Response({
                "message": "wrong board id"
            }, status=status.HTTP_404_NOT_FOUND)
            return response

        serializer = BoardDetailSerializer(board, many=True)

        data = serializer.data
        response = Response({
            "data": data
        }, status=status.HTTP_200_OK)
        return response

# 게시판 카테고리 생성


class CreateBoardCategoryViewSet(APIView):

    def post(self, request):

        serializer = CreateBoardCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        response = Response({
            "message": "create board category successfully"
        }, status=status.HTTP_201_CREATED)
        return response


# 게시글 생성 삭제
class CreateBoardViewSet(APIView):

    def post(self, request):

        serializer = CreateBoardSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        response = Response({
            "message": "create board successfully",
            "boards_id" : serializer.data['id'],
        }, status=status.HTTP_201_CREATED)

        return response


class DeleteBoardsViewSet(APIView):

    def delete(self, request, boards_id):

        user_id = int(request.data["user_id"])
        board = Boards.objects.get(id=boards_id)
        # 게시글 삭제시 작성자 확인
        if board.boards_writer.id != user_id:
            response = Response({
                "message": "bad access (user not allowed)"
            }, status=status.HTTP_403_FORBIDDEN)
            return response

        board.delete_date = timezone.now()
        board.save()
        response = Response({
            "message": "delete success",
        }, status=status.HTTP_200_OK)

        return response


# 게시판 댓글 생성 삭제
class CreateCommentsViewSet(APIView):

    def post(self, request):

        serializer = CreateCommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        response = Response({
            "message": "create comments successfully"
        }, status=status.HTTP_201_CREATED)

        return response


class DeleteCommentsViewSet(APIView):

    def delete(self, request, comments_id):

        user_id = request.data["user_id"]
        comment = Comments.objects.get(id=comments_id)
        # 댓글 삭제시 작성자 확인
        if comment.comments_writer.id != int(user_id):
            response = Response({
                "message": "bad access (user not allowed)",
            }, status=status.HTTP_403_FORBIDDEN)
            return response

        comment.delete_date = timezone.now()
        comment.save()
        response = Response({
            "message": "delete success",
        }, status=status.HTTP_200_OK)

        return response


########################## 부가기능 ############################

class BoardsLikeViewSet(APIView):

    def post(self, request):

        boards_id = request.data["likes_board"]
        user_id = request.data["likes_user"]
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
