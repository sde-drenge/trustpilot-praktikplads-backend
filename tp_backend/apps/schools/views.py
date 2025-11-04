from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from tp_backend.middleware.customview import CustomAPIView

from .serializers import SchoolSerializer, SchoolCreatorSerializer
from .models import School


# Create your views here.
class GetAllSchools(CustomAPIView):
    """
    Get:
    ```
    []
    ```
    """

    serializer_class = SchoolSerializer

    def get(self, request, *args, **kwargs):
        schools = School.objects.all()
        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSpecificSchool(CustomAPIView):
    """
    Get a specific school by uuid
    Get:
    ```
    {
        "uuid": "school-uuid",
        "name": "School Name",
        "domain": "school.domain",
        "isActive": true,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z"
    }
    ```
    """

    serializer_class = SchoolSerializer

    def get(self, request, *args, **kwargs):
        school_uuid = request.query_params.get("uuid")
        school = get_object_or_404(School, uuid=school_uuid)
        serializer = SchoolSerializer(school)
        return Response(serializer.data, status=status.HTTP_200_OK)
