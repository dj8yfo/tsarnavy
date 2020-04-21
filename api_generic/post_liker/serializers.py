from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(email=validated_data["email"], username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id"]


class PostSerializer(serializers.ModelSerializer):
    author = UserNameSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["title", "author", "body", "created", "id"]
        extra_kwargs = {"created": {"read_only": True}}
