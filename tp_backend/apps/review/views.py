from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from tp_backend.middleware.customview import CustomAPIView

from user.constants import Roles
from .serializers import ReviewSerializer
from .models import Review


# Create your views here.
class GetAllReviews(CustomAPIView):
    """
    Get:
    ```
    []
    ```
    """
    authenticationRequired = False
    
    serializer_class = ReviewSerializer

    @method_decorator(csrf_exempt, name="dispatch")
    def get(self, request, *args, **kwargs):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class GetSpecificReview(CustomAPIView):
    """
    Get a specific review by uuid
    Get:
    ```
    {
        "uuid": "review-uuid",
        "student": {
            "uuid": "student-uuid",
            "email": "student@example.com",
            "name": "Student Name",
            "role": "student",
            "isActive": true,
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z"
        },
        "title": "Review Title",
        "content": "Review Content",
        "rating": 5,
        "isApproved": true,
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z"
    }
    ```
    """
    
    authenticationRequired = False

    serializer_class = ReviewSerializer

    @method_decorator(csrf_exempt, name="dispatch")
    def get(self, request, *args, **kwargs):
        review_uuid = request.query_params.get("uuid")
        review = get_object_or_404(Review, uuid=review_uuid)
        serializer = ReviewSerializer(review, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CreateReview(CustomAPIView):
    """
    Create a new review
    Post:
    ```
    {
        "title": "Review Title",
        "content": "Review Content",
        "rating": 5,
        "isApproved": true
    }
    ```
    """

    serializer_class = ReviewSerializer
    
    roleNeeded = Roles.accessToCreateReviews

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid()
        review = serializer.save()
        response_serializer = self.serializer_class(review, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class GetAllReviewsFromStudent(CustomAPIView):
    """
    Get all reviews from a specific student by student uuid
    Get:
    ```
    [
        {
            "uuid": "review-uuid",
            "student": {
                "uuid": "student-uuid",
                "email": "student@example.com",
                "name": "Student Name",
                "role": "student",
                "isActive": true,
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z"
            },
            "title": "Review Title",
            "content": "Review Content",
            "rating": 5,
            "isApproved": true,
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z"
        }
    ]
    ```
    """
    
    authenticationRequired = True
    
    serializer_class = ReviewSerializer
    
    roleNeeded = Roles.canGetStudentFromReview

    def get(self, request, *args, **kwargs):
        student_uuid = request.query_params.get("uuid")
        reviews = Review.objects.filter(student__uuid=student_uuid)
        serializer = ReviewSerializer(reviews, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)