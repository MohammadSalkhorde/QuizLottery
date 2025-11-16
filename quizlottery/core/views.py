from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, generics

from .models import Comments, Timer, Org
from .serializers import (
    CommentSerializer,
    CommentCreateSerializer,
    TimerSerializer,
    OrgSerializer
)

class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        return Response({
            "message": "نظر شما با موفقیت ثبت شد و پس از تایید نمایش داده می‌شود",
            "comment": res.data
        }, status=201)

class CommentListAPIView(generics.ListAPIView):
    queryset = Comments.objects.filter(is_active=True).order_by('-register_date')
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]


class TimerListAPIView(generics.ListAPIView):
    queryset = Timer.objects.filter(is_active=True)
    serializer_class = TimerSerializer
    permission_classes = [AllowAny]

class OrgListAPIView(generics.ListAPIView):
    queryset = Org.objects.filter(is_active=True)
    serializer_class = OrgSerializer
    permission_classes = [AllowAny]

class OrgDetailAPIView(generics.RetrieveAPIView):
    queryset = Org.objects.filter(is_active=True)
    serializer_class = OrgSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
