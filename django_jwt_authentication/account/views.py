from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from account.serializers import UserRegistrationSerializer


# Generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user=user)
    
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }

# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response(data={"token": token, "message" : "Registration Successful"}, status=status.HTTP_201_CREATED)