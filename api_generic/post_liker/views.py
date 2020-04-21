from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSignupView(APIView):
    permission_classes = (~IsAuthenticated,)

    def post(self, request, format=None):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            User.objects.create_user(
                serialized.initial_data["username"],
                serialized.initial_data["email"],
                serialized.initial_data["password"],
            )
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class UserObtainToken(APIView):
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (BasicAuthentication, JWTAuthentication)
    # from django.conf.settings.REST_FRAMEWORK

    def post(self, request, format=None):
        token_pair = TokenObtainPairSerializer.get_token(request.user)
        result = {}
        result["refresh"] = str(token_pair)
        result["access"] = str(token_pair.access_token)

        return Response(result, status=status.HTTP_200_OK)
