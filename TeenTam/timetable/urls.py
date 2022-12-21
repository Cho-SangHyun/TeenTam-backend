from django.urls import path
from . import views

app_name = "timetable"

urlpatterns = [
    path('', views.TimeTableViewSet.as_view(), name="boards_list"),
]
