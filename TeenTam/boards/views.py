from rest_framework.views import APIView

# Create your views here.

class BoardListViewSet(APIView):

    def get(self, request):
        return request