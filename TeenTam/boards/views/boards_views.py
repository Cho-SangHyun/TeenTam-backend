from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Boards
from account.models import User
from mypage.models import Bookmark
from ..serializer import *
from django.utils import timezone
from datetime import datetime, timedelta



# 카테고리별 게시글 목록
class BoardsListViewSet(APIView):   

    def get(self, request, boards_category):

        page = int(request.GET.get('page'))
        offset = int(request.GET.get('offset'))
        order = request.GET.get('order')
        cursor = (page-1)*offset

        # 게시글 모든 카테고리 조회
        if boards_category == 0:
            sql = ('SELECT * FROM boards_boards AS boards WHERE boards.delete_date IS NULL ORDER BY '
                   + order + ' DESC LIMIT ' + str(offset) + ' OFFSET ' + str(cursor))
            boards_num = Boards.objects.filter(
                delete_date=None).count()  # 전체 게시글 갯수
        # 게시글 특정 카테고리 조회
        else:
            sql = ('SELECT * FROM boards_boards AS boards WHERE boards.boards_category_id = ' +
                   str(boards_category) + ' AND boards.delete_date IS NULL ORDER BY ' + order + ' DESC LIMIT ' +
                   str(offset) + ' OFFSET ' + str(cursor))
            boards_num = Boards.objects.filter(
                boards_category=boards_category, delete_date=None).count()  # 카테고리 내 전체 게시글 갯수

        boards = Boards.objects.raw(sql)

        serializer = BoardsListSerializer(boards, many=True)

        data = serializer.data
        response = Response({
            "message": "GET boards list success",
            "data": data,
            "boards_num": boards_num,
        })

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


# 게시글 생성
class CreateBoardViewSet(APIView):

    def post(self, request):

        serializer = CreateBoardsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            # 유저 작성 댓글 갯수 갱신
            user_id = request.data['boards_writer']
            user = User.objects.get(id=user_id)
            user.boards_written += 1
            user.save()

            serializer.save()

        response = Response({
            "message": "create board successfully",
            "boards_id": serializer.data['id'],
        }, status=status.HTTP_201_CREATED)

        return response


# 게시글 삭제
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


# 게시글 상세보기
class BoardDetailViewSet(APIView):

    def get(self, request, boards_category, boards_id):

        board = Boards.objects.filter(id=boards_id).first()
        user_id = request.GET.get("user_id")
        bookmark = Bookmark.objects.filter(bookmark_user_id=user_id, bookmark_boards_id=boards_id).first()
        
        # 사용자 북마크 여부
        if bookmark:
            is_bookmark = True
        else:
            is_bookamrk = False
            
        # 없는 게시글 요청 시
        if board is None:
            response = Response({
                "message": "wrong board id"
            }, status=status.HTTP_404_NOT_FOUND)
            return response

        # 삭제된 게시글 요청 시
        if board.delete_date is not None:
            response = Response({
                "message": "deleted board id"
            }, status=status.HTTP_204_NO_CONTENT)
            return response

        serializer = BoardDetailSerializer(board)
        data = serializer.data

        """
        조회수 기능 - 토큰 사용
        매일 00시에 만료되는 토큰에 클라이언트가 조회한 boards_id 저장
        만약, 조회한 게시글 id가 이미 쿠키에 존재할 경우 hit 증가 X
        """
        # 토큰 만료시간 설정, 매일 00시에 만료
        expire_date, now = datetime.now(), datetime.now()
        expire_date += timedelta(days=1)
        expire_date = expire_date.replace(
            hour=0, minute=0, second=0, microsecond=0)
        expire_date -= now
        max_age = expire_date.total_seconds()  # 토큰 만료시간

        cookie_value = request.COOKIES.get('hitboard', '_')

        if f'_{board.id}_' not in cookie_value:
            cookie_value += f'{board.id}_'
            board.hit += 1
            board.save()

        response = Response({
            "data": data,
            "bookmark": bookmark,
        }, status=status.HTTP_200_OK)
        response.set_cookie('hitboard', value=cookie_value,
                            max_age=max_age, httponly=True, samesite=None)

        return response


# 게시글 수정
class ModifyBoardsViewSet(APIView):

    def post(self, request, boards_id):

        # 작성자 Validation
        board = Boards.objects.filter(id=boards_id).first()

        if board.boards_writer.id != int(request.data['user_id']):
            response = Response({
                "message": "bad access (user not allowed)",
            }, status=status.HTTP_403_FORBIDDEN)
            return response

        serializer = ModifyBoardsSerializer(board, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        response = Response({
            "message": "modify board success",
            "boards_id": serializer.data['id']
        })

        return response
