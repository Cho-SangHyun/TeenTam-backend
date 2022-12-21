from rest_framework import serializers
from .models import TimeTable
from account.models import User


class TimeTableSerializer(serializers.ModelSerializer):

    class Meta:

        model = TimeTable
        fields = ["timetable_user", "period", "day", "subject"]
