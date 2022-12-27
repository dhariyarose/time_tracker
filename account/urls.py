from . import views
from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token
from django.contrib.auth import views as auth_views
urlpatterns = [
 path('signup/', views.Signup.as_view(), name='signup'),
 path('login/', views.UserLogin.as_view(), name='user_login'),
 path('users-list/', views.UserList.as_view(), name='user_list'),
 path('manage-user/<int:id>/', views.ManageUser.as_view(), name='manage_user'),

]
