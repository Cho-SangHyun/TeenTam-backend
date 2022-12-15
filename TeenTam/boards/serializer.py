from rest_framework import serializers
from .models import Boards, Comments, BoardCategories, Likes

# 댓글 정보
class CommentsSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='comments_writer.username')

    class Meta:

        model = Comments
        fields = ['id', 'username', 'content', 'comments_writer',
                  'like', 'pub_date', 'modify_date', 'delete_date']


# 게시판별 게시글 목록
class BoardsListSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='boards_writer.username')

    class Meta:

        model = Boards
        fields = ['username', 'boards_writer', 'title', 'hit', 'like', 'pub_date',
                  'boards_category', 'image_exist', 'id', 'content', 'comments_num']

# 게시글 수정


class ModifyBoardsSerializer(serializers.ModelSerializer):

    class Meta:

        model = Boards
        fields = ['id', 'title', 'content']

    def update(self, instance, validated_data):

        instance.title = validated_data['title']
        instance.content = validated_data['content']
        instance.save()

        return instance

# 게시글 생성


class CreateBoardsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Boards
        fields = ['id', 'boards_category', 'title', 'content', 'boards_writer']

    def validate(self, data):

        category_name = data['boards_category']
        boards_category = BoardCategories.objects.filter(name=category_name)

        if boards_category is None:
            raise serializers.ValidationError("wrong category name")

        return data


# 게시글 상세보기
class BoardDetailSerializer(serializers.ModelSerializer):

    comments = CommentsSerializer(many=True, read_only=True)
    writer_username = serializers.CharField(source='boards_writer.username')
    boards_category_name = serializers.CharField(source="boards_category.name")
    # category_name = BoardCategoriesSerializer(read_only = True)

    class Meta:

        model = Boards
        fields = ['comments', 'title', 'content', 'pub_date', 'delete_date',
                  'modify_date', 'image_exist', 'like', 'hit', 'comments_num',
                  'is_main', 'boards_category', 'boards_category_name', 'writer_username', 'boards_writer']

    def validate(self, data):

        delete_date = data['delete_date']
        if delete_date is not None:
            raise serializers.ValidationError("this board already deleted")

        return data


# 게시판 카테고리
class BoardCategoriesSerializer(serializers.ModelSerializer):

    class Meta:

        model = BoardCategories
        fields = ['name', 'description',
                  'delete_date', 'manager_id', 'create_date']


# 게시판 카테고리 생성
class CreateBoardCategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = BoardCategories
        fields = ['name', 'description']

# 댓글 생성


class CreateCommentsSerializer(serializers.ModelSerializer):

    class Meta:

        model = Comments
        fields = ['content', 'comments_board', 'comments_writer']

    def create(self, validated_data):

        # 게시글 댓글 갯수 ++
        board_id = validated_data['comments_board'].id
        board = Boards.objects.get(id=board_id)
        board.comments_num += 1
        board.save()

        return super().create(validated_data)

# 댓글 수정


class ModifyCommentsSerializer(serializers.ModelSerializer):

    class Meta:

        model = Comments
        fields = ['content']

    def update(self, instance, validated_data):

        instance.content = validated_data['content']
        instance.save()

        return instance

# 좋아요 기능


class LikesSerializer(serializers.ModelSerializer):

    class Meta:

        model = Likes
        fields = "__all__"
