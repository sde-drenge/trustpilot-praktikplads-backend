from django.urls import include, path, re_path
from rest_framework import routers

router = routers.DefaultRouter()

from . import views

def get_urls():
    """Append custom urls"""
    urls = router.urls
    
    urls.append(
        re_path(
            r"^get-specific-company/$",
            views.GetSpecificCompany.as_view(),
            name="get_specific_company_view",
        )
    )
    
    
    urls.append(
        re_path(
            r"^create-company/$",
            views.CreateCompany.as_view(),
            name="create_company_view",
        )
    )
    
    urls.append(
        re_path(
            r"^get-company-by-name/$",
            views.GetCompanyByName.as_view(),
            name="get_company_by_name_view",
        )
    )

    return urls


urlpatterns = [
    path(
        "", views.GetAllCompanies.as_view(), name="get_all_companies_view"
    ),
    re_path(r"^", include(get_urls())),
]