from http.client import HTTPResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import authentication, permissions
from web import serializers
from web.models import TEST_MODEL
from web.serializers import TestModelSerializer, TitleModelSerializer


class webHomeViewSet(APIView):
    def get(self, request):
        qd = TEST_MODEL.objects.all()
        serializer = TestModelSerializer(qd, many=True)
        # json = JSONRenderer().render(serializer.data)
        print(serializer.data)
        return render(request, "test.html")

    def post(self, request):
        print(request.data)
        TestSerializer = TestModelSerializer(data=request.data)
        TestSerializer.is_valid()
        TitleSerializer = TitleModelSerializer(data=request.data)
        TitleSerializer.is_valid()
        TestSerializer.save()
        TitleSerializer.save()
        return HttpResponse("POST")
