from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .serializers import PostSerializer, ActionSerializer
from .models import Post, Action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import create_action


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
        create_action(request.user, "logged in ", request.user)

        return Response(result, status=status.HTTP_200_OK)


class PostsViewset(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            newpost = serializer.save(author=request.user)
            create_action(request.user, "created", newpost)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=True)
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user not in post.users_like.all():
            post.users_like.add(request.user)
            create_action(request.user, "liked", post)
            return Response({"liked": True}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {post.id: "already liked"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=["post"], detail=True)
    def unlike(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user in post.users_like.all():
            post.users_like.remove(request.user)
            create_action(request.user, "unliked", post)
            return Response({"unliked": True}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {post.id: "disgusting, right?"}, status=status.HTTP_400_BAD_REQUEST
            )


# auxiliary
class ActionViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)
