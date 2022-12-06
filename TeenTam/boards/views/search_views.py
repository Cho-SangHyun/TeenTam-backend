from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from ..models import Boards
from account.models import User
from ..serializer import *
from django.db.models import Q
from TeenTam.utils import BadRequest

# 키워드 검색
class SearchBoardsViewSet(APIView):

    def get(self, request):

        page = int(request.GET.get('page')) # 페이지 넘버
        offset = int(request.GET.get('offset')) # offset 한 페이지에 보여주는 목록 갯수
        order = request.GET.get('order') # 정렬 기능
        keyword = request.GET.get('keyword') # 검색 키워드
        category_name = request.GET.get('category_name') # 카테고리 명 
        writer_name = request.GET.get('writer_name')
        # print(category_name)
        q = Q()
        # 카테고리 내 검색일 경우
            
        # 글쓴이 검색일 경우
        if writer_name:
            boards_writer = User.objects.filter(username=writer_name).first()
            if boards_writer:
                q &= Q(boards_writer=boards_writer.id)
                if category_name:
                    category = BoardCategories.objects.filter(name=category_name).first()
                    if not category:
                        response = BadRequest("wrong category_id")
                        return response
                    q &= Q(boards_category = category.id)
                    q &= Q(is_anon = False)
                    
                boards = Boards.objects.filter(q).distinct().order_by(order)
            else:
                boards  = []
            
        # 게시글 검색일 경우   
        else:
            q |= Q(title__icontains=keyword)
            q |= Q(content__icontains=keyword)
            
            if category_name:
                category = BoardCategories.objects.filter(name=category_name).first()
                if not category:
                    response = BadRequest("wrong category_id")
                    return response
                q &= Q(boards_category = category.id)
                
            boards = Boards.objects.filter(q).distinct().order_by(order)
                
        paginator = Paginator(boards, offset)
        boards_list = paginator.page(page)
        serializers = BoardsListSerializer(boards_list, many=True)
        data = serializers.data

        response = Response({
            "data": data,
            "boards_num": len(boards), # 전체 검색 결과 갯수
            "message": "search board list success",
        })

        return response
