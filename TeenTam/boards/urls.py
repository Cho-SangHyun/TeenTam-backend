from django.urls import path
from boards.views import boards_views, search_views, comments_views, like_views

app_name = "boards"

urlpatterns = [
     # ---------------------- BOARDS ----------------------#
    path('<int:boards_category>/', boards_views.BoardsListViewSet.as_view(),
         name="boards_list"),  # 게시판
    path('<int:boards_category>/id/<int:boards_id>/',
         boards_views.BoardDetailViewSet.as_view(), name="boards_detail"),  # 게시글 상세보기
    path('delete-board/<int:boards_id>/',
         boards_views.DeleteBoardsViewSet.as_view(), name="delete-board"),
    path('create-board/', boards_views.CreateBoardViewSet.as_view(), name="create-board"),
    path('create-board-category/', boards_views.CreateBoardCategoryViewSet.as_view(),
         name="create-board-category"),
    path('board-modify/<int:boards_id>/', boards_views.ModifyBoardsViewSet.as_view(), name="modify-board"),
    
     # ---------------------- COMMENTS ----------------------#
    path('create-comment/', comments_views.CreateCommentsViewSet.as_view(),
         name="create-comment"),
    path('delete-comment/<int:comments_id>/',
         comments_views.DeleteCommentsViewSet.as_view(), name="delete-comment"),
    path('comment-modify/<int:comments_id>/', comments_views.ModifyCommentsViewSet.as_view(), name="modify-comment"),
    
     # ---------------------- LIKES ----------------------# 
    path('like-board/', like_views.BoardsLikeViewSet.as_view(), name="like-board"),
    # path('like-comment/', views.CommentsLikeViewSet.as_view(), name="like-comment"),
    
     # ---------------------- SEARCH ----------------------# 
    path('search-boards/', search_views.SearchBoardsViewSet.as_view(), name="search_boards_list"),
    
]
