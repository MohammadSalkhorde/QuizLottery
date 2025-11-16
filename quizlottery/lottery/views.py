from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import QuestionListSerializer, AnswerQuestionSerializer
from .models import Questions

class QuestionListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = Questions.objects.filter(is_active=True)
        serializer = QuestionListSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AnswerQuestionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        correct = serializer.save()
        if correct:
            return Response({"message": "پاسخ صحیح بود و شما به لاتاری اضافه شدید"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "پاسخ اشتباه بود"}, status=status.HTTP_200_OK)
