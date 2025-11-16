from django.urls import path
from .views import QuestionListAPIView, AnswerQuestionAPIView

urlpatterns = [
    path('questions/', QuestionListAPIView.as_view(), name='question-list'),
    path('questions/answer/', AnswerQuestionAPIView.as_view(), name='answer-question'),
]
