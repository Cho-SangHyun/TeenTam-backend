from dataclasses import fields
from rest_framework import serializers
from web.models import TEST_MODEL, TITLE_MODEL


class TestModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TEST_MODEL
        fields = ["context"]


class TitleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TITLE_MODEL
        fields = ["title"]
