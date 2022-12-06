from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from django.core.paginator import Paginator
from ..serializer import *
from account.serializer import UserMainSerializer
from boards.serializer import BoardsListSerializer
from boards.models import Boards


# 마이페이지 메인화면
class MypageMainViewSet(APIView):
            
    def get(self, request, user_id):

        user = User.objects.get(id=user_id)
        serializer = UserMainSerializer(user)
        data = serializer.data

        response = Response({
            "message": "GET Mypage Main success",
            "data": data,
        }, status=status.HTTP_200_OK)

        return response


class ChangePasswordViewSet(APIView):

    '''
    새 비밀번호
    새 비밀번호 확인 << 클라이언트 사이드에서 처리
    기존 비밀번호
    '''

    def post(self, request):

        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid()

        response = Response({
            "message": "Password Changed Successfully"
        }, status=status.HTTP_200_OK)

        return response


class ChangeUsernameViewSet(APIView):

    '''
    닉네임 변경
    닉네임 변경 주기는 한달로 is_changed를 통해 
    갱신 가능한 날짜를 저장.
    클라이언트 측에서 datetime << 데이터를 보내야함
    '''

    # 남은 시간 표기를 위한 닉네임 변경 가능 일자 response
    def get(self, request):
        user_id = request.GET.get("user_id")
        user = User.objects.get(id=user_id)
        serializer = ChangeUsernameDatetimeSerializer(user)
        data = serializer.data

        response = Response({
            "data": data,
            "message": "Username Changed Successfully"
        }, status=status.HTTP_200_OK)

        return response

    def post(self, request):

        serializer = ChangeUsernameSerializer(data=request.data)
        serializer.is_valid()

        response = Response({
            "message": "username modified successfully"
        }, status=status.HTTP_200_OK)

        return response


class ModifyUserInformationViewSet(APIView):

    def post(self, request):

        serializer = ModifyUserInformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        response = Response({
            "message": "user information modified successfully"
        }, status=status.HTTP_200_OK)

        return response


class MyBoardsListViewSet(APIView):

    def get(self, request):

        user_id = request.GET.get('user_id')
        page = request.GET.get('page')

        boards = Boards.objects.filter(
            boards_writer=user_id).order_by("-pub_date")
        boards_num = boards.count()
        paginator = Paginator(boards, 10)
        boards_list = paginator.page(page)

        serializers = BoardsListSerializer(boards_list, many=True)
        data = serializers.data

        response = Response({
            "data": data,
            "boards_num": boards_num,
            "message": "GET myboards list success",
        })

        return response
