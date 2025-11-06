from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer

from .models import Company

User = get_user_model()


class CompanySerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True, format="hex")
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, allow_null=True, required=False, default="")
    website = serializers.URLField(allow_blank=True, allow_null=True, required=False)
    createdAt = serializers.DateTimeField(read_only=True)
    createdBy = UserSerializer(read_only=True)
    vat_number = serializers.CharField(max_length=9)

    class Meta:
        model = Company
        fields = [
            "uuid",
            "name",
            "description",
            "website",
            "createdBy",
            "createdAt",
            "updatedAt",
            "vat_number",
        ]
        read_only_fields = [
            "uuid",
            "createdBy",
            "createdAt",
            "updatedAt",
            "vat_number",
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

        return super().create(validated_data)