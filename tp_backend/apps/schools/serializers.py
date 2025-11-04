from rest_framework import serializers

from .models import School

class SchoolSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True, format="hex")
    name = serializers.CharField()
    domain = serializers.CharField()
    isActive = serializers.BooleanField()
    createdAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = School
        fields = [
            "uuid",
            "name",
            "domain",
            "isActive",
            "createdAt",
            "updatedAt",
        ]
        read_only_fields = [
            "uuid",
            "createdAt",
            "updatedAt",
        ]


class SchoolCreatorSerializer(SchoolSerializer):
    class Meta:
        model = School
        fields = (
            "name",
            "domain",
        )