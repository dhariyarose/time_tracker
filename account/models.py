from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=20, unique=False, null=True, blank=True)
    designation = models.CharField(max_length=200, null=True,blank=True)
    GENDER_TYPE_CHOICES = (
    ("male", "male"),
    ("female", "female"),
    )
    gender = models.CharField(max_length=10, null=True,blank=True,choices=GENDER_TYPE_CHOICES)
    profile_picture = models.FileField(null=True,blank=True,upload_to="uploads/profile_picture")
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def is_admin(self):
        found = self.groups.filter(name='admin').count()
        if found > 0:
            return True
        return False
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = uuid.uuid4()
        super(CustomUser, self).save(*args, **kwargs)

from django.contrib.auth import get_user_model
User = get_user_model()