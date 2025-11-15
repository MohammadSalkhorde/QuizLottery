from rest_framework import serializers
from django.contrib.auth import get_user_model
import random

User = get_user_model()


# ----------------- ارسال کد -----------------
class SendCodeSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11)

    def validate_mobile_number(self, value):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("شماره موبایل معتبر نیست")
        return value

    def create(self, validated_data):
        mobile = validated_data['mobile_number']

        user, created = User.objects.get_or_create(
            mobile_number=mobile,
            defaults={'is_active': False, 'name':'', 'family':''}
        )

        user.active_code = str(random.randint(10000, 99999))
        user.is_active = False
        user.save()

        print(f"Activation code sent to {mobile}: {user.active_code}")
        return user


# ----------------- تایید کد و login/register -----------------
from rest_framework_simplejwt.tokens import RefreshToken

class VerifyCodeSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        mobile = attrs.get("mobile_number")
        code = attrs.get("code")

        try:
            user = User.objects.get(mobile_number=mobile)
        except User.DoesNotExist:
            raise serializers.ValidationError("کاربر یافت نشد")

        if user.active_code != code:
            raise serializers.ValidationError("کد فعال‌سازی اشتباه است")

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        user.is_active = True
        user.active_code = None
        user.save()
        return user

# ----------------- اطلاعات کاربر (Protected) -----------------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "mobile_number",
            "name",
            "family",
            "email",
            "gender",
            "province",
            "city",
            "is_active",
            "is_admin",
            "register_date",
            "image_name",
            "cover_image",
            "national_id",
            "national_id_image"
        ]
        
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    family = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "name",
            "family",
            "email",
            "gender",
            "province",
            "city",
            "image_name",
            "national_id",
            "national_id_image"
        ]
        extra_kwargs = {
            "email": {"required": False},
            "gender": {"required": False},
            "province": {"required": False},
            "city": {"required": False},
            "image_name": {"required": False},
            "national_id": {"required": False},
            "national_id_image": {"required": False},
        }


class SendPasswordChangeCodeSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11)

    def validate_mobile_number(self, value):
        try:
            user = User.objects.get(mobile_number=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("کاربر یافت نشد")
        return value

    def create(self, validated_data):
        user = User.objects.get(mobile_number=validated_data['mobile_number'])
        user.active_code = str(random.randint(10000, 99999))
        user.save()
        print("Password change OTP:", user.active_code)
        return user
    
class VerifyPasswordChangeSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=6)

    def validate(self, attrs):
        try:
            user = User.objects.get(mobile_number=attrs['mobile_number'])
        except User.DoesNotExist:
            raise serializers.ValidationError("کاربر یافت نشد")

        if user.active_code != attrs['code']:
            raise serializers.ValidationError("کد تأیید اشتباه است")

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.active_code = None
        user.save()
        return user
