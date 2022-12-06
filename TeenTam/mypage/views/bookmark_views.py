from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Bookmark
from ..serializer import BookmarkSerializer
from ..validation import BookmarkValidation
from TeenTam.utils import BadRequest

# 북마크 생성

class ToggleBookmarkViewSet(APIView):
    
    def post(self, request):
        user_id = request.data["bookmark_user_id"]
        boards_id = request.data["bookmark_boards_id"]
        
        bookmark = Bookmark.objects.filter(bookmark_user_id=user_id, bookmark_boards_id=boards_id).first()
        # 이미 북마크 존재 시 삭제 
        if bookmark:
            bookmark.delete()
            response  = Response({
                "message" : "bookmark deleted successfully",
            },status=status.HTTP_202_ACCEPTED)
        
            return response
        # 잘못된 boards_id (이미 삭제된 경우 포함)
        if not BookmarkValidation(boards_id):
            
            response = BadRequest("wrong boards_id")        
            return response
        
        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print("save?")
            serializer.save()
        
        response = Response({
            "message" : "bookmark registered succuessfully",
        }, status=status.HTTP_201_CREATED)
        return response