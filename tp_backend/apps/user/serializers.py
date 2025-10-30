from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .constants import Roles
from .models import User

class UserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True, format="hex")
    name = serializers.CharField()
    createdAt = serializers.DateTimeField(read_only=True)
    isActive = serializers.BooleanField()
    
    class Meta:
        model = User
        fields = [
            "uuid",
            "email",
            "name",
            "isActive",
            "role",
            "createdAt",
            "updatedAt",
        ]
        read_only_fields = [
            "uuid",
            "createdAt",
            "updatedAt",
        ]

class UserCreatorSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "email",
        )
        
    def get_user(self, email, exclude=None):
        user = None
        user = User.objects.filter(email__iexact=email, deletedAt__isnull=True)
        if exclude:
            user.exclude(uuid=exclude)
        user = user.first()
        return user
    
    def validate_email(self, value):
        # Ensure the user doesn't already exist
        email = value.lower()
        user: User | None = self.get_user(email)
        if user:
            raise serializers.ValidationError(
                _("A user with this e-mail already exists. Try to login.")
            )

        return email