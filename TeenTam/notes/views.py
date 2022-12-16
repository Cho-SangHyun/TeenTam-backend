from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import NotesSerializer, NotesContentSerializer
from account.serializer import UserOnlyUsernameSerializer
from .models import Notes
from account.models import User
from django.db.models import Q


class NotesViewSet(APIView):

    def post(self, request):
        # 'sender', 'receiver', 'content'
        serializer = NotesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        response = Response({
            "message": "send notes successfully"
        }, status=status.HTTP_201_CREATED)
        return response

    def get(self, request):

        user_id = request.GET.get("user_id")

        sender_user = Notes.objects.only("receiver").filter(
            sender=user_id).distinct().values_list("receiver")
        receiver_user = Notes.objects.only("sender").filter(
            receiver=user_id).distinct().values_list("sender")

        user_values_list = sender_user.union(receiver_user, all=False)
        user_list = []
        for user in user_values_list:
            user_list.append(user[0])

        user = User.objects.filter(id__in=user_list)
        serializer = UserOnlyUsernameSerializer(user, many=True)

        response = Response({
            "message": "get notes user list successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        return response


class NotesContentViewSet(APIView):

    def get(self, request):

        user_id = request.GET.get("user_id")
        notes_user_id = request.GET.get("notes_user_id")
        notes = Notes.objects.order_by("send_date").filter(
            Q(sender=user_id, receiver=notes_user_id) | Q(sender=notes_user_id, receiver=user_id))
        serializer = NotesContentSerializer(notes, many=True)
        data = serializer.data

        response = Response({
            "message": "get notes content successfully",
            "data": data
        })
        return response
