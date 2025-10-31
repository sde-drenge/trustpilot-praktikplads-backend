import datetime

import jwt
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from tp_backend.middleware.customview import CustomAPIView

from .serializers import UserCreatorSerializer, UserSerializer
from .models import User


@method_decorator(csrf_exempt, name="dispatch")
class SignUpView(CustomAPIView):
    """
    Post Data:
    ```
    {
        "name": "name",
        "email": "email",
        "password": "password",
        "password2": "password2",
    }
    ```
    """

    permission_classes = ()
    authentication_classes = ()
    authenticationRequired = False
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        inputData = request.data
        password = inputData.get("password")
        password2 = inputData.get("password2")
        if password != password2 or not password:
            data = {"error": "Passwords do not match"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserCreatorSerializer(data=inputData)
        if serializer.is_valid():
            serializer.save()
            user = serializer.instance
            user.set_password(password)
            user.generateVerificationCode()
            user.save()

            token = Token.objects.create(user=user)
            payload = {
                "user_id": user.id,
                "exp": datetime.datetime.now() + datetime.timedelta(days=1),
                "iat": datetime.datetime.now(),
                "token": token.key,
            }
            jwtToken = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            response = Response()
            response.set_cookie("jwt", jwtToken)
            data = self.serializer_class(user).data
            data["jwtToken"] = jwtToken
            response.data = data
            return response
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
        
        
@method_decorator(csrf_exempt, name="dispatch")
class LoginView(CustomAPIView):
    """
    Post Data:
    {
        "email": "email",
        "password": "password",
    }
    """

    permission_classes = ()
    authentication_classes = ()
    authenticationRequired = True
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        inputData = request.data
        user = get_object_or_404(User, email=inputData.get("email"))
        if not user.check_password(inputData.get("password")):
            data = {"error": "Invalid password"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            data = {"error": "User is not active"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        token, created = Token.objects.get_or_create(user=user)
        payload = {
            "user_id": user.id,
            "exp": datetime.datetime.now().astimezone() + datetime.timedelta(days=1),
            "iat": datetime.datetime.now().astimezone(),
            "token": token.key,
        }
        jwtToken = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        response = Response(status=200)
        response.set_cookie("jwt", jwtToken)

        data = self.serializer_class(user).data
        data["jwtToken"] = jwtToken
        response.data = data
        return response
