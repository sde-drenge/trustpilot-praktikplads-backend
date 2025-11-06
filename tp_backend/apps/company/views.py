from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from tp_backend.middleware.customview import CustomAPIView
from user.constants import Roles

from .models import Company
from .serializers import CompanySerializer

# Create your views here.
class GetAllCompanies(CustomAPIView):
    """
    Get:
    ```
    []
    ```
    """
    
    authenticationRequired = False
    
    serializer_class = CompanySerializer

    @method_decorator(csrf_exempt, name="dispatch")
    def get(self, request, *args, **kwargs):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSpecificCompany(CustomAPIView):
    """
    Get a specific company by uuid
    Get:
    ```
    {
        "uuid": "company-uuid",
        "name": "Company Name",
        "description": "Company Description",
        "isActive": true,
        "createdBy": "user-uuid",
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z"
    }
    ```
    """
    
    authenticationRequired = False

    serializer_class = CompanySerializer

    @method_decorator(csrf_exempt, name="dispatch")
    def get(self, request, *args, **kwargs):
        company_uuid = request.query_params.get("uuid")
        company = get_object_or_404(Company, uuid=company_uuid)
        serializer = CompanySerializer(company, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CreateCompany(CustomAPIView):
    """
    Create a new company
    Post:
    ```
    {
        "name": "Company Name",
        "description": "Company Description",
        "vat_number": "12345678"
    }
    ```
    Response:
    ```
    {
        "uuid": "company-uuid",
        "name": "Company Name",
        "description": "Company Description",
        "isActive": true,
        "createdBy": "user-uuid",
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z"
    }
    ```
    """
    serializer_class = CompanySerializer
    
    roleNeeded = Roles.accesstoCreateCompanies

    def post(self, request, *args, **kwargs):
        serializer = CompanySerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            company = serializer.save()
            return Response(
                CompanySerializer(company, context={"request": request}).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class GetCompanyByName(CustomAPIView):
    """
    Get a specific company by name
    Get:
    ```
    {
        "uuid": "company-uuid",
        "name": "Company Name",
        "description": "Company Description",
        "isActive": true,
        "createdBy": "user-uuid",
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z"
    }
    ```
    """
    
    authenticationRequired = False

    serializer_class = CompanySerializer

    @method_decorator(csrf_exempt, name="dispatch")
    def get(self, request, *args, **kwargs):
        company_name = request.query_params.get("name")
        if not company_name:
            return Response({"detail": "Missing 'name' query parameter."}, status=status.HTTP_400_BAD_REQUEST)

        company_name = company_name.strip()
        company = get_object_or_404(Company, name__iexact=company_name)
        serializer = CompanySerializer(company, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)