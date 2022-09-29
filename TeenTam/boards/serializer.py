from rest_framework import serializers
from .models import Boards, Comments, BoardCategories


class CommentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Comments
        fields = ['content', 'comments_writer', 'like', 'pub_date', 'modify_date', 'delete_date']


class BoardDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = BoardCategories
        depth = 1
    


class CreateBoardSerializer(serializers.ModelSerializer):
    
    # comments = CommentsSerializer(many=True, read_only=True)
    # board_category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    
    class Meta:
        model = Boards
        fields = ['boards_category', 'title', 'content','boards_writer']
        
class CreateBoardCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BoardCategories
        fields = ['name', 'description']
        