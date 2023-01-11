from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import TimeTableSerializer
from .models import TimeTable
from account.models import User
from .utils import StringToArray
import json


class TimeTableViewSet(APIView):

    def post(self, request):

        timetable = request.data["timetable"]
        user_id = request.data["user_id"]

        for cls in timetable:
            timetable = TimeTable.objects.filter(
                period=cls['period'], day=cls['day'], timetable_user=cls['timetable_user']).first()
            if timetable:
                timetable.subject = cls['subject']
                timetable.save()
                continue

            serializer = TimeTableSerializer(data=cls)
            if serializer.is_valid():
                serializer.save()

        response = Response({
            "message": "create timetable successfully"
        }, status=status.HTTP_201_CREATED)
        return response

    def get(self, request):
        #---------Param--------#
        user_id = request.GET.get("user_id")

        timetable = TimeTable.objects.filter(timetable_user=user_id)
        serializer = TimeTableSerializer(timetable, many=True)
        response = Response({
            "message": "tiemtable get successfully",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

        return response

    def delete(self, request):
        
        timetable = request.data["timetable"]
        
        for cls in timetable:
            t = TimeTable.objects.filter(timetable_user=cls["timetable_user"], period=cls["period"], day=cls["day"])
            if t:
                t.delete()
                message = "timetable delete successfully"
            else:
                message = "wrong timetable"
                
        response = Response({
            "message" : message,
        },status=status.HTTP_200_OK)
        return  response