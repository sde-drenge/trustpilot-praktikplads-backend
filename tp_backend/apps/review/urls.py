from django.urls import include, path, re_path
from rest_framework import routers

router = routers.DefaultRouter()

from . import views

def get_urls():
    """Append custom urls"""
    urls = router.urls

    urls.append(
        re_path(
            r"^get-specific-review/$",
            views.GetSpecificReview.as_view(),
            name="get_specific_review_view",
        )
    )
    
    urls.append(
        re_path(
            r"^create-review/$",
            views.CreateReview.as_view(),
            name="create_review_view",
        )
    )
    
    urls.append(
        re_path(
            r"^get-all-reviews-from-student/$",
            views.GetAllReviewsFromStudent.as_view(),
            name="get_all_reviews_from_student_view",
        )
    )

    return urls


urlpatterns = [
    path(
        "", views.GetAllReviews.as_view(), name="get_all_reviews_view"
    ),
    re_path(r"^", include(get_urls())),
]