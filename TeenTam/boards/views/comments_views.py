from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.paginator import Paginator
from ..models import Comments
from account.models import User
from ..serializer import *
from django.utils import timezone


# 댓글 생성
class CreateCommentsViewSet(APIView):

    def post(self, request):

        serializer = CreateCommentsSerializer(data=request.data)
        if serializer.is_valid():

            # 유저 작성 댓글 갯수 갱신
            user = User.objects.get(id=request.data['comments_writer'])
            user.comments_written += 1
            user.save()

            serializer.save()

        commentsList = Comments.objects.filter(
            comments_board_id=request.data['comments_board'])
        commentSerializer = CommentsSerializer(commentsList, many=True)

        response = Response({
            "data": commentSerializer.data,
            "message": "create comment success"
        }, status=status.HTTP_201_CREATED)

        return response


# 댓글 삭제
class DeleteCommentsViewSet(APIView):

    def delete(self, request, comments_id):

        comment = Comments.objects.get(id=comments_id)
        # 댓글 삭제시 작성자 확인
        if comment.comments_writer.id != int(request.data["user_id"]):
            response = Response({
                "message": "bad access (user not allowed)",
            }, status=status.HTTP_403_FORBIDDEN)
            return response

        comment.delete_date = timezone.now()
        comment.save()
        response = Response({
            "message": "delete comment success",
        }, status=status.HTTP_200_OK)

        return response


# 댓글 수정
class ModifyCommentsViewSet(APIView):

    def post(self, request, comments_id):

        # 작성자 Validation
        comment = Comments.objects.filter(id=comments_id).first()

        # 작성자와 수정자 불일치
        if comment.comments_writer.id != int(request.data['user_id']):
            response = Response({
                "message": "bad access (user not allowed)",
            }, status=status.HTTP_403_FORBIDDEN)
            return response

        serializer = ModifyCommentsSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        response = Response({
            "message": "modify board success",
            "boards_id": comment.comments_board_id,
        })

        return response
