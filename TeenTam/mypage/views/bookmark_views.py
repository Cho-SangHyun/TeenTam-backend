from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Bookmark
from ..serializer import BookmarkSerializer
from ..validation import BookmarkValidation
from TeenTam.utils import BadRequest
from boards.models import Boards
from boards.serializer import BoardsListSerializer
from django.core.paginator import Paginator


# 북마크 생성

class BookmarkViewSet(APIView):

    def post(self, request):
        #--------Body--------#
        user_id = request.data["bookmark_user_id"]
        boards_id = request.data["bookmark_boards_id"]

        bookmark = Bookmark.objects.filter(
            bookmark_user_id=user_id, bookmark_boards_id=boards_id).first()
        # 이미 북마크 존재 시 삭제
        if bookmark:
            bookmark.delete()
            response = Response({
                "message": "bookmark deleted successfully",
            }, status=status.HTTP_202_ACCEPTED)

            return response
        # 잘못된 boards_id (이미 삭제된 경우 포함)
        if not BookmarkValidation(boards_id):

            response = BadRequest("wrong boards_id")
            return response

        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        response = Response({
            "message": "bookmark registered succuessfully",
        }, status=status.HTTP_201_CREATED)
        return response

    def get(self, request):
        #--------Param---------#
        user_id = request.GET.get("user_id")
        page = request.GET.get("page")
        offset = 10  # 이부분은 하드코딩 offset 10으로 고정. 추후에 변동 가능

        bookmarkList = Bookmark.objects.order_by(
            "-bookemark_date").filter(bookmark_user_id=user_id)
        boards_id_list = []
        for bookmark in bookmarkList:
            boards_id_list.append(bookmark.bookmark_boards_id)

        # bookmark boards list Paginate
        boards = Boards.objects.filter(id__in=boards_id_list)
        paginator = Paginator(boards, offset)
        boards_list = paginator(page)

        serializer = BoardsListSerializer(boards_list, many=True)
        data = serializer.data

        response = Response({
            "message": "bookmar list get successfully",
            "data": data,
        }, status=status.HTTP_200_OK)
        return response
