from .models import  CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import Group
import re
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('email', 'password','confirm_password','first_name','last_name','phone_number','gender','designation')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        errors = []
        if not password or not confirm_password:
            errors.append("Please enter a password and confirm it.")
        if password != confirm_password:
            errors.append("Those passwords don't match.")
        if errors:
            raise serializers.ValidationError({"errors": errors})
        if len(password) < 8 :
            errors.append("This password is too short. It must contain at least 8 characters")
        if ' ' in password:
            errors.append("Password should not contain space.")
        if re.search('[A-Z]', password)==None or re.search('[a-z]', password)==None or re.search('[0-9]', password)==None or re.search('[^A-Za-z0-9]', password)==None:
            errors.append("This password is not strong. Your password must contain at least 1 number, 1 uppercase, 1 lowercase and 1 special character.")
        if errors:
            raise serializers.ValidationError({"errors": errors})
        return data

    def create(self, validated_data):
        email = validated_data['email']
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','phone_number','profile_picture','first_name','last_name','email','gender','designation')
        depth = 1
