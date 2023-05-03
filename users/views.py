from django.shortcuts import render
from rest_framework import generics, status
from .models import Freelancer, Client, User
from .serializers import UserSerializer, FreelanceSignupSerializer, ClientSignupSerializer
from rest_framework.response import Response
from rest_framework.authtoken.views import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsClientUser, IsFreelancerUser
from rest_framework import permissions
# Create your views here.


class FreelanceSignupView(generics.GenericAPIView):
    serializer_class = FreelanceSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': Token.objects.get(user=user).key,
            'message': "Account create Successfully!"
        })

class ClientSignupView(generics.GenericAPIView):
    serializer_class = ClientSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': Token.objects.get(user=user).key,
            'message': "Account create Successfully!"
        })

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_client': user.is_client
        })


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

class ClientOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsClientUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class FreelancerOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsFreelancerUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user