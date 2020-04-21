from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Action


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
    users_like = UserNameSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["title", "author", "body", "created", "id", "users_like"]
        extra_kwargs = {"created": {"read_only": True}}


class ActionTargetSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return {"model": str(type(value)), "value": str(value), "id": value.id}


class ActionSerializer(serializers.ModelSerializer):
    target = ActionTargetSerializer(read_only=True)
    user = UserNameSerializer(read_only=True)

    class Meta:
        model = Action
        fields = ["user", "verb", "target", "created"]
