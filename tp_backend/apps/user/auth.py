import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission

from .constants import Roles
from .models import User


class CustomTokenAuthentication(authentication.BaseAuthentication):
    """
    Add this header:
    Authorization: Token <Token>
    """

    keyword = "Token"
    model = None
    authenticationRequired = True

    def __init__(self, authenticationRequired=True):
        self.authenticationRequired = authenticationRequired

    def authenticate(self, request):
        jwtKey = request.COOKIES.get("jwt")

        if jwtKey is None:
            jwtKey = authentication.get_authorization_header(request).split()
            if jwtKey is None or len(jwtKey) != 2:
                return None

            if jwtKey[0].decode() != self.keyword:
                return None
            jwtKey = jwtKey[1]

        try:
            userDetails = jwt.decode(jwtKey, settings.SECRET_KEY, algorithms="HS256")
        except Exception as e:
            if self.authenticationRequired:
                msg = "Invalid Token"
                raise exceptions.AuthenticationFailed(msg)
            else:
                return (None, None)

        if (
            not userDetails
            or not userDetails.get("user_id")
            or not userDetails.get("token")
        ):
            msg = "Invalid Login Credentials"
            raise exceptions.AuthenticationFailed(msg)

        user = User.objects.filter(id=userDetails.get("user_id")).first()
        if not user:
            msg = "Invalid Login Credentials"
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = "User is not verified"
            raise exceptions.AuthenticationFailed(msg)

        userToken = Token.objects.filter(user=user).first()
        if not userToken:
            msg = "Invalid Token"
            raise exceptions.AuthenticationFailed(msg)

        token = userDetails.get("token")
        if token != userToken.key:
            msg = "Invalid Token"
            raise exceptions.AuthenticationFailed(msg)

        if user.deleted_at is not None:
            msg = "This user has been deleted. Please contact support for more information"
            raise exceptions.AuthenticationFailed(msg)

        # if request type is get then update last activity
        if request.method == "GET":
            user.updateLastActivity()
        return (user, token)


class IsPermissionsHigherThanUser(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user.role in Roles.higherThanUser)


class IsUserAdmin(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user.role == Roles.ADMIN)
