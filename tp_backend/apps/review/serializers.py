from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator 
from user.serializers import UserSerializer
from user.constants import Roles
 

from .models import Review

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True, format="hex")
    student = UserSerializer(read_only=True)
    title = serializers.CharField(max_length=54)
    content = serializers.CharField(max_length=500)
    rating = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    isApproved = serializers.BooleanField(default=True)
    createdAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "uuid",
            "student",
            "title",
            "content",
            "rating",
            "isApproved",
            "createdAt",
            "updatedAt",
        ]
        read_only_fields = [
            "uuid",
            "student",
            "createdAt",
            "updatedAt",
        ]
        
    def create(self, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user", None) if request is not None else None
        
        print("Creating review for user:", user)
        
        validated_data["student"] = user

        return super().create(validated_data)

    