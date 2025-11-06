
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator 
from user.serializers import UserSerializer
from company.serializers import CompanySerializer
from company.models import Company


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

    # Accept a company UUID on write, but return nested company data on read.
    company = CompanySerializer(read_only=True)
    company_uuid = serializers.UUIDField(write_only=True, required=False, allow_null=True, format='hex')

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
            "company",
            "company_uuid",
        ]
        read_only_fields = [
            "uuid",
            "student",
            "createdAt",
            "updatedAt",
            "company",
        ]
        extra_kwargs = {
            'company_uuid': {'write_only': True}
        }
        
    def validate_company_uuid(self, value):
        """Convert a UUID to a Company instance or raise a validation error."""
        if value is None:
            return None
        try:
            company = Company.objects.get(uuid=value)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Company with provided UUID does not exist.")
        return company

    def validate(self, attrs):
        """Move write-only company_uuid (Company instance after field validation) into 'company'.

        DRF will call validate_company_uuid and replace company_uuid value with the Company
        instance. We must pop it and put it on 'company' so model creation doesn't receive
        an unexpected keyword argument.
        """
        company = attrs.pop('company_uuid', None)
        if company is not None:
            attrs['company'] = company
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user", None) if request is not None else None
        validated_data["student"] = user

        return super().create(validated_data)

    