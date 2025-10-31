from django.conf import settings
from ..apps.user.permissions import UserPermissions

from .decrypter import RequestTimeLoggingMiddleware


class CustomAPIView(UserPermissions, RequestTimeLoggingMiddleware):
    authenticationRequired = True
    roleNeeded = None
    noPermissionForMethods = []

    def __init__(self, **kwargs) -> None:
        if self.authenticationRequired == False:
            self.permission_classes = ()
        super().__init__(**kwargs)

    def get_authenticators(self):
        """
        Instantiates and returns the list of authenticators that this view can use.
        """
        return [
            auth(authenticationRequired=self.authenticationRequired)
            for auth in self.authentication_classes
        ]