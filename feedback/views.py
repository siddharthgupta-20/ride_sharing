from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Feedback
from .serializers import FeedbackSerializer

# Create your views here.

class CreateFeedbackView(APIView):
    def post(self,request):
        serializer = FeedbackSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
