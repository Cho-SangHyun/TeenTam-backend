from django.urls import path
from . import views


app_name = "boards"

urlpatterns = [
    path('<int:boards_category>/', views.BoardListViewSet.as_view(),
         name="boards_list"),  # 게시판
    path('<int:boards_category>/id/<int:boards_id>/',
         views.BoardDetailViewSet.as_view(), name="boards_detail"),  # 게시글 상세보기
    path('create-board/', views.CreateBoardViewSet.as_view(), name="create-board"),
    path('create-board-category/', views.CreateBoardCategoryViewSet.as_view(),
         name="create-board-category"),
    path('create-comment/', views.CreateCommentsViewSet.as_view(),
         name="create-comment"),
    path('delete-board/<int:boards_id>/',
         views.DeleteBoardsViewSet.as_view(), name="delete-board"),
    path('delete-comment/<int:comments_id>/',
         views.DeleteCommentsViewSet.as_view(), name="delete-comment"),
    path('like-board/', views.BoardsLikeViewSet.as_view(), name="like-board"),
    # path('like-comment/', views.CommentsLikeViewSet.as_view(), name="like-comment"),




]
