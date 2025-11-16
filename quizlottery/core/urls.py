from django.urls import path
from .views import (
    CommentCreateAPIView,
    CommentListAPIView,
    TimerListAPIView,
    OrgListAPIView,
    OrgDetailAPIView
)

urlpatterns = [
    path("comments/", CommentListAPIView.as_view()),         
    path("comments/create/", CommentCreateAPIView.as_view()),

    path("timers/", TimerListAPIView.as_view()),             

    path("orgs/", OrgListAPIView.as_view()),                
    path("orgs/<int:id>/", OrgDetailAPIView.as_view()),      
]
