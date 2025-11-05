from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer

from .models import School

User = get_user_model()


class SchoolSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True, format="hex")
    name = serializers.CharField()
    owner = UserSerializer(read_only=True)
    description = serializers.CharField(allow_blank=True, allow_null=True, required=False, default="")
    domain = serializers.CharField(validators=[UniqueValidator(queryset=School.objects.all())])
    createdAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = School
        fields = [
            "uuid",
            "name",
            "description",
            "domain",
            "isActive",
            "owner",
            "createdBy",
            "createdAt",
            "updatedAt",
        ]
        read_only_fields = [
            "uuid",
            "createdBy",
            "createdAt",
            "updatedAt",
        ]
        
    def create(self, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user", None) if request is not None else None

        if not user or not getattr(user, "is_authenticated", False):
            account = self.context.get("account")
            if not account:
                raise serializers.ValidationError("Authenticated user or account context required.")
            user = User.objects.filter(uuid=account).first()
            if not user:
                raise serializers.ValidationError("Invalid account context provided.")
        
        # ensure description is present in validated_data (use default if omitted)
        validated_data.setdefault("description", "")
        validated_data["createdBy"] = user
        validated_data["owner"] = user

        return super().create(validated_data)

