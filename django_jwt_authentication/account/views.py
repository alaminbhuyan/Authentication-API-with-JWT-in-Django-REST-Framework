from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from account.serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer)


# Generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user=user)

    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }

# Create your views here.

# User Registration class


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response(data={"token": token, "message": "Registration Successful"}, status=status.HTTP_201_CREATED)

# User Login class


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            token = get_tokens_for_user(user)
            return Response(data={"token": token, "message": "Login Successful"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"errors": {"non_field_errors": ['Email or password not valid']}}, status=status.HTTP_404_NOT_FOUND)


# User Profile class
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(instance=request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
