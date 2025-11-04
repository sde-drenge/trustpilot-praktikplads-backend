from django.urls import include, path, re_path
from rest_framework import routers

router = routers.DefaultRouter()

from . import views

def get_urls():
    """Append custom urls"""
    urls = router.urls

    urls.append(
        re_path(
            r"^get-specific-school/$",
            views.GetSpecificSchool.as_view(),
            name="get_specific_school_view",
        )
    )

    return urls


urlpatterns = [
    path(
        "", views.GetAllSchools.as_view(), name="get_all_schools_view"
    ),
    re_path(r"^", include(get_urls())),
]