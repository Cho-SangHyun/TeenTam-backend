from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import TimeTableSerializer
from .models import TimeTable

class TimeTable(APIView):
    
    def post(self, request):
        
        serializer = TimeTableSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
        response = Response({
            "message" : "timetable created successfully"
        }, status=status.HTTP_201_CREATED)
        
        return response
    
    def get(self, request):
        #---------Param--------#
        user_id = request.GET.get("user_id")
        
        timetable = TimeTable.objects.filter(timetable_user_id=user_id)
        serializer = TimeTableSerializer(timetable)
        
        response = Response({
            "message" : "tiemtable get successfully",
            "data" : serializer.data
        }, status=status.HTTP_200_OK)
        
        return response    