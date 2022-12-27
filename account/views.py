from functools import partial
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView    
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class Signup(CreateAPIView):
    # register an user with email

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : True,
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        
        return Response(response, status=status_code)

class UserLogin(APIView):
    #login with email and password

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        if email and CustomUser.objects.filter(email=email):
            user = authenticate(username=email, password=password)
            if not user:
                response = {
                        'status_code':  status.HTTP_400_BAD_REQUEST,
                        'message': "A user with this email and password is not found.",
                        'status':"password_wrong"
                        }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            user_obj = CustomUser.objects.get(email=email)
            payload = JWT_PAYLOAD_HANDLER(user_obj)
            jwt_token = JWT_ENCODE_HANDLER(payload)
        
            profile = UserSerializer(user_obj).data
        
            profile['user_id'] = user_obj.id
            response = {
                'success' : True,
                'status code' : status.HTTP_200_OK,
                'message': 'User logged in  successfully',
                'token' : jwt_token,
                'profile':profile
            }
            status_code = status.HTTP_200_OK
            return Response(response, status=status_code)
        else:
            response = {
                'status_code':  status.HTTP_400_BAD_REQUEST,
                'message': "A user with this email is not found.",
                'status':"wrong_email"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    """
    List all users
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, format=None):
        users = CustomUser.objects.filter(is_active=True)
        serializer = UserSerializer(users, many=True)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'status_code': status_code,
            'data': serializer.data
            }
        return Response(response)


class ManageUser(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get_object(self, id):
        try:
            return CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'status_code': status_code,
            'data': serializer.data
            }
        return Response(response)

    def put(self, request, id, format=None):
        try:
            user = self.get_object(id)
            serializer = UserSerializer(user, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'status_code': status_code,
                    'data': serializer.data
                    }
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                    'success': False,
                    'status_code': status_code,
                    'errors': serializer.errors
                    }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'error': str(e)
                }
        return Response(response, status=status_code)

    def delete(self, request, id, format=None):
        try:
            user = self.get_object(id)
            user.is_active=False #Cannot delete some instances of model 'CustomUser' because they are referenced through protected foreign key.
            user.save()
            status_code = status.HTTP_204_NO_CONTENT
            response = {
                'success':True,
                'status_code': status_code
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'error': str(e)
                }
        return Response(response, status=status_code)
