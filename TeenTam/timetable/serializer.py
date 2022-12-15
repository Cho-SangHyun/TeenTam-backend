from rest_framework import serializers
from .models import TimeTable
from account.models import User

class TimeTableSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = TimeTable
        fields = ["timetable_user_id", "timetable", "school", "grade", "room"]
        
    def validate(self, data):
        
        school = data["school"]
        grade = data["grade"]
        user_id = data["timetable_user_id"]
        
        user = User.objects.filter(id=user_id).first()
        if user.school is None or user.grade is None:
            raise serializers.ValidationError("please fill the school and grade")
        
        if user.school != school or user.grade != grade:
            raise serializers.ValidationError("wrong school or grade")
        
        return data
