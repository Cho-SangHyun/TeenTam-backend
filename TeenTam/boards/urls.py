from django.urls import path
from . import views


app_name = "boards"

urlpatterns = [
    path('boards-category/<int:boards_ctg>/',views.BoardListViewSet.as_view(),name="boards_list"), # 게시판 
    path('<int:boards_id>/',views.BoardDetailViewSet.as_view(),name="boards_detail"), # 게시글 상세보기
    path('create-board/',views.CreateBoardViewSet.as_view(), name="create-board"),
    path('create-board-category/',views.CreateBoardCategoryViewSet.as_view(), name="create-board-category"),  
    path('create-comment/', views.CreateCommentsViewSet.as_view(), name="create-comment"),
]