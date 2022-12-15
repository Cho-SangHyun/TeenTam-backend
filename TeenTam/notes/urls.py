from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path('', views.NotesViewSet.as_view()),
    path('content/', views.NotesContentViewSet.as_view()),
]
