from rest_framework import serializers
from django.utils import timezone
from boards.models import Boards

class BookmarkSerializer(serializers.Serializer):
    
    user_id = serializers.IntegerField(require=True)
    boards_id = serializers.IntegerField(require=True)
    bookmark_date = serializers.DateTimeField(default=timezone.now)
    
    def validate(self, data):
        
        boards_id = data["boards_id"]
        boards = Boards.objects.filter(id=boards_id).first()
        if not boards or boards.delete_date:
            raise serializers.ValidationError("wrong boards_id or deleted board")
        
        return data