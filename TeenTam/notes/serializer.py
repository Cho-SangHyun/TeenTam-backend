from rest_framework import serializers
from .models import Notes


class NotesSerializer(serializers.ModelSerializer):

    class Meta:

        model = Notes
        fields = ['sender', 'receiver', 'content']

    def validate(self, data):

        if data['sender'] == data['receiver']:
            raise serializers.ValidationError("wrong sender, receiver")
        return data


class NotesContentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Notes
        fields = ['sender', 'content', 'send_date']
