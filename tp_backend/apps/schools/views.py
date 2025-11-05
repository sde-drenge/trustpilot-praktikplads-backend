from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from tp_backend.middleware.customview import CustomAPIView

from user.constants import Roles
from .serializers import SchoolSerializer
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


class CreateSchool(CustomAPIView):
    """
    Create a new school
    Post:
    ```
    {
        "name": "School Name",
        "domain": "school.domain",
        "description?": "Optional description of the school"
    }
    ```
    Response:
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
    roleNeeded = Roles.accessToCreateSchools
    
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        school = serializer.save()
        response_serializer = SchoolSerializer(school, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
