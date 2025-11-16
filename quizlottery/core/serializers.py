from rest_framework import serializers
from .models import Comments, Timer, Org
from accounts.models import CustomUser

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.mobile_number", read_only=True)

    class Meta:
        model = Comments
        fields = [
            "id",
            "user",
            "text",
            "register_date",
            "is_active",
        ]

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["text"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Comments.objects.create(
            user=user,
            text=validated_data["text"],
            is_active=False 
        )

class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = [
            "id",
            "title",
            "start_time",
            "end_time",
            "is_active",
        ]

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = [
            "id",
            "title",
            "description",
            "image",
            "phone",
            "address",
            "link",
            "is_active",
        ]
