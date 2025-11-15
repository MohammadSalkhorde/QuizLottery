from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


# ----------------- ارسال کد -----------------
class SendCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "کد تأیید ارسال شد"}, status=status.HTTP_200_OK)


# ----------------- تایید کد / login-register -----------------
class VerifyCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "حساب شما فعال شد",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)


# ----------------- خروج -----------------
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "با موفقیت خارج شدید"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "توکن معتبر نیست"}, status=status.HTTP_400_BAD_REQUEST)

# ----------------- اطلاعات کاربر (Protected) -----------------
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "پروفایل شما به‌روزرسانی شد",
            "profile": UserProfileSerializer(request.user).data
        }, status=status.HTTP_200_OK)


class SendPasswordChangeCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendPasswordChangeCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "کد تغییر رمز ارسال شد"}, status=status.HTTP_200_OK)

class VerifyPasswordChangeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyPasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "رمز عبور با موفقیت تغییر کرد"}, status=status.HTTP_200_OK)
    

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "با موفقیت خارج شدید"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "توکن نامعتبر"}, status=status.HTTP_400_BAD_REQUEST)