from account.models import CustomUser
from rest_framework import serializers
from .models import *
from account.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name','description')

class ProjectDetailSerializer(serializers.ModelSerializer):
    created_user_name = serializers.SerializerMethodField()
    updated_user_name = serializers.SerializerMethodField()

    def get_created_user_name(self,obj):
        return obj.created_by.first_name+" "+obj.created_by.last_name

    def get_updated_user_name(self,obj):
        if obj.updated_by:
            return obj.updated_by.first_name+" "+obj.updated_by.last_name
        return ""

    class Meta:
        model = Project
        fields = ('__all__')

class ProjectTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = ('__all__')
    
class ProjectTaskDetailSerializer(serializers.ModelSerializer):
    created_user = serializers.SerializerMethodField()
    updated_user = serializers.SerializerMethodField()
    user_assigned = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()

    def get_created_user(self,obj):
        return UserSerializer(obj.created_by).data

    def get_updated_user(self,obj):
        if obj.updated_by:
            return UserSerializer(obj.created_by).data
        return ""

    def get_user_assigned(self,obj):
        if obj.fk_user_assigned:
            return UserSerializer(obj.fk_user_assigned).data
        return ""

    def get_project(self,obj):
        return ProjectDetailSerializer(obj.fk_project).data

    class Meta:
        model = ProjectTask
        exclude = ('fk_project','fk_user_assigned','created_by','updated_by')


class UserWorkTimeLogDetailSerializer(serializers.ModelSerializer):
    task = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_task(self,obj):
        return ProjectTaskDetailSerializer(obj.fk_task).data
    
    def get_user(self,obj):
        return UserSerializer(obj.fk_user).data


    class Meta:
        model = UserWorkTimeLog
        fields = ('__all__')

class UserWorkTimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkTimeLog
        fields = ('__all__')

class InvolvedUserLogsSerializer(serializers.ModelSerializer):
    logs = serializers.SerializerMethodField()

    def get_logs(self,obj):
        logs_obj =UserWorkTimeLog.objects.filter(fk_task__fk_project=self.project,fk_user=obj).order_by('-start_time')
        return UserWorkTimeLogDetailSerializer(logs_obj,many=True).data

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super(InvolvedUserLogsSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ('id','first_name','last_name','designation','email','phone_number','logs')