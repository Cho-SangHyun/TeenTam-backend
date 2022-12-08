from django.urls import path
from .views import user_info_views, bookmark_views, profile_image_views

app_name = "mypage"

urlpatterns = [
    #--------------USER INFO--------------#
    path('<int:user_id>/', user_info_views.MypageMainViewSet.as_view()),
    path('<int:user_id>/modify-info/', user_info_views.ModifyUserInformationViewSet.as_view()),
    path('myboardslists/', user_info_views.MyBoardsListViewSet.as_view()),
    path('change-password/', user_info_views.ChangePasswordViewSet.as_view()),
    
    #--------------BOOKMARK--------------#
    path('bookmark/', bookmark_views.BookmarkViewSet.as_view()),
    
    #--------------PROFILE IMAGE UPLOAD--------------#
    path('profile-image-upload/', profile_image_views.UploadProfileImage.as_view()),
    path('profile-image-url/', profile_image_views.GetProfileImage.as_view()),
]    
