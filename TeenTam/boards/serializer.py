from wsgiref import validate
from django.forms import CharField
from rest_framework import serializers
from .models import Boards, Comments, BoardCategories


class CommentsSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source = 'comments_writer.username')
    
    class Meta:
        
        model = Comments
        fields = ['username', 'content', 'comments_writer', 'like', 'pub_date', 'modify_date', 'delete_date']


class BoardCategoriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = BoardCategories
        fields = ['name', 'description', 'delete_date', 'manager_id', 'create_date']


class BoardDetailSerializer(serializers.ModelSerializer):
    
    comments = CommentsSerializer(many=True, read_only=True)
    writer_username = serializers.CharField(source = 'boards_writer.username')
    # category_name = BoardCategoriesSerializer(read_only = True)
    
    class Meta:
        
        model = Boards
        fields = ['comments','title', 'content', 'pub_date', 'delete_date',
                  'modify_date', 'image_exist', 'like', 'hit', 'comments_num',
                  'is_main', 'boards_category', 'writer_username', 'boards_writer']



class CreateBoardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Boards
        fields = ['boards_category', 'title', 'content','boards_writer']
        
    def validate(self, data):
        
        category_name = data['boards_category']
        boards_category = BoardCategories.objects.filter(name = category_name)
        if boards_category is None:
            raise serializers.ValidationError("wrong category name")
        
        return data
        

class CreateBoardCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BoardCategories
        fields = ['name', 'description']


class CreateCommentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comments
        fields = ['content', 'comments_board', 'comments_writer']
        
    def create(self, validated_data):
        
        # 게시글 댓글 갯수 ++
        board_id = validated_data['comments_board'].id
        board = Boards.objects.get(id = board_id)
        board.comments_num += 1
        board.save()
        
        return super().create(validated_data)
    
    

        