from django.conf import settings
from ..apps.user.permissions import UserPermissions

from .decrypter import RequestTimeLoggingMiddleware


class CustomAPIView(UserPermissions, RequestTimeLoggingMiddleware):
    authenticationRequired = True
    roleNeeded = None
    noPermissionForMethods = []

    def __init__(self, **kwargs) -> None:
        # If authentication is not required for this view, clear
        # authentication and permission classes so DRF doesn't try to
        # instantiate authenticators or enforce permissions.
        if self.authenticationRequired == False:
            self.permission_classes = ()
            # ensure no authenticators are used
            self.authentication_classes = ()
        super().__init__(**kwargs)

    def get_authenticators(self):
        """
        Instantiates and returns the list of authenticators that this view can use.
        """
        # DRF authentication classes do not accept view-specific kwargs
        # in their constructor. Instantiate without arguments. If this view
        # has authentication disabled, return an empty list.
        if not getattr(self, "authenticationRequired", True):
            return []

        return [auth() for auth in getattr(self, "authentication_classes", ())]