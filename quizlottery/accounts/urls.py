from django.urls import path
from .views import *

urlpatterns = [
    path('send-code/', SendCodeAPIView.as_view(), name='send-code'),
    path('verify-code/', VerifyCodeAPIView.as_view(), name='verify-code'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('password/send-code/', SendPasswordChangeCodeAPIView.as_view(), name='send-password-code'),
    path('password/verify-code/', VerifyPasswordChangeAPIView.as_view(), name='verify-password-code'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
