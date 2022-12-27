from datetime import datetime, date
from functools import partial
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from account.models import CustomUser
import calendar
from account.serializers import UserSerializer
from django.db.models import Sum

class ProjectList(APIView):
    """
    List all projects, or create a new project.
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectDetailSerializer(projects, many=True)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'status_code': status_code,
            'data': serializer.data
            }
        return Response(response)

    def post(self, request, format=None):
        try:
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                obj.created_by=request.user
                obj.save()
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


class ProjectDetail(APIView):
    """
    Retrieve, update or delete a project instance.
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get_object(self, slug):
        try:
            return Project.objects.get(slug=slug)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        project = self.get_object(slug)
        serializer = ProjectDetailSerializer(project)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'status_code': status_code,
            'data': serializer.data
            }
        return Response(response)

    def put(self, request, slug, format=None):
        try:
            project = self.get_object(slug)
            serializer = ProjectSerializer(project, data=request.data,partial=True)
            if serializer.is_valid():
                obj = serializer.save()
                obj.updated_by=request.user
                obj.save()
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

    def delete(self, request, slug, format=None):
        try:
            project = self.get_object(slug)
            project.delete()
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


class ProjectRelatedUserList(APIView):
    """
    List all users related to the project, or add users to the project or delete an user from the list.
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, slug, format=None):
        project = Project.objects.get(slug=slug)
        users_ids = ProjectRelatedUser.objects.filter(fk_project=project).values_list('fk_user',flat=True)
        users = CustomUser.objects.filter(id__in=users_ids)
        serializer = UserSerializer(users, many=True)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'status_code': status_code,
            'data': serializer.data
            }
        return Response(response)

    def post(self, request, slug, format=None):
        try:
            project = Project.objects.get(slug=slug)
            users_id = request.data.get('users_id')
            if users_id:
                users = CustomUser.objects.filter(id__in=users_id)
                for user in users:
                    if not ProjectRelatedUser.objects.filter(fk_user=user,fk_project=project):
                        ProjectRelatedUser.objects.create(fk_user=user,fk_project=project)
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'status_code': status_code,
                    }
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                    'success': False,
                    'status_code': status_code,
                    'errors': "please add users"
                    }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'error': str(e)
                }
        return Response(response, status=status_code)

    def delete(self, request, slug, format=None):
        try:
            project = Project.objects.get(slug=slug)
            user_id = request.data.get('user_id')
            user = CustomUser.objects.get(id=user_id)
            related_user_obj = ProjectRelatedUser.objects.get(fk_user=user,fk_project=project)
            related_user_obj.delete()
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


class ProjectTaskList(APIView):
    """
    List all tasks of a project, or create a new task.
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, slug, format=None):
        project = Project.objects.get(slug=slug)
        tasks = ProjectTask.objects.filter(fk_project=project)
        serializer = ProjectTaskDetailSerializer(tasks, many=True)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'status_code': status_code,
            'data': serializer.data
            }
        return Response(response)

    def post(self, request, slug, format=None):
        try:
            project = Project.objects.get(slug=slug)
            request.data._mutable = True
            data = request.data
            data['fk_project']=project.id
            data['status'] = "to_do"
            serializer = ProjectTasksSerializer(data=data)
            if serializer.is_valid():
                obj = serializer.save()
                obj.created_by=request.user
                obj.save()
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

class MyTasks(APIView):
    """
    Get assigned tasks of an logged user.
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, format=None):
        if request.GET.get('project'):
            slug = request.GET.get('project')
            project = Project.objects.get(slug=slug)
            tasks = ProjectTask.objects.filter(fk_project=project,fk_user_assigned=request.user)
        else:
            tasks = ProjectTask.objects.filter(fk_user_assigned=request.user)
        serializer = ProjectTaskDetailSerializer(tasks, many=True)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'status_code': status_code,
            'data': serializer.data
            }
        return Response(response)

class ProjectTaskDetail(APIView):
    """
    Retrieve, update or delete a task instance. also update the task status 
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get_object(self, slug):
        try:
            return ProjectTask.objects.get(slug=slug)
        except ProjectTask.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        project = self.get_object(slug)
        serializer = ProjectTaskDetailSerializer(project)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'status_code': status_code,
            'data': serializer.data
            }
        return Response(response)

    def put(self, request, slug, format=None):
        try:
            project = self.get_object(slug)
            serializer = ProjectTasksSerializer(project, data=request.data,partial=True)
            if serializer.is_valid():
                obj = serializer.save()
                obj.updated_by=request.user
                obj.save()
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

    def delete(self, request, slug, format=None):
        try:
            task = self.get_object(slug)
            task.delete()
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



class UserTimeLogList(APIView):
    """
    List all logs of an user, or create a new log.
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, format=None):
        logs = UserWorkTimeLog.objects.filter(fk_user=request.user).order_by('-start_time')
        serializer = UserWorkTimeLogDetailSerializer(logs, many=True)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'status_code': status_code,
            'data': serializer.data
            }
        return Response(response)

    def post(self, request, format=None):
        try:
            request.data._mutable = True
            data = request.data
            data['fk_user'] = request.user.id
            data['fk_task'] = request.data.get('task_id')
            serializer = UserWorkTimeLogSerializer(data=data)
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


class UserTimeLogManage(APIView):
    """
    Retrieve, update or delete a log instance of an user(can not edit others).
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get_object(self, id):
        try:
            return UserWorkTimeLog.objects.get(id=id)
        except UserWorkTimeLog.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        log = self.get_object(id)
        serializer = UserWorkTimeLogDetailSerializer(log)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'status_code': status_code,
            'data': serializer.data
            }
        return Response(response)

    def put(self, request, id, format=None):
        try:
            log = self.get_object(id)
            if log.fk_user != request.user:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                    'success': False,
                    'status_code': status_code,
                    'errors': "You are unable to edit other people's log."
                    }
            else:
                serializer = UserWorkTimeLogSerializer(log, data=request.data,partial=True)
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
            log = self.get_object(id)
            if log.fk_user != request.user:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                    'success': False,
                    'status_code': status_code,
                    'errors': "You are unable to delete other people's log."
                    }
            else:
                log.delete()
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


class ProjectInvolvedUserLogs(APIView):
    """
    List all users related to the project and their logs
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, slug, format=None):
        project = Project.objects.get(slug=slug)
        users_ids = ProjectRelatedUser.objects.filter(fk_project=project).values_list('fk_user',flat=True)
        users = CustomUser.objects.filter(id__in=users_ids)
        serializer = InvolvedUserLogsSerializer(users, many=True,project=project)
        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'status_code': status_code,
            'data': serializer.data
            }
        return Response(response)

class UsersMonthlyLog(APIView):
    """
    Get monthly logs of users with details of task, projects , how many hours they worked per day etc
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, format=None):
        month = request.GET.get('month')
        year = request.GET.get('year')
        if not month:
            month = datetime.now().month
            year = datetime.now().year
        users = CustomUser.objects.filter(is_active=True)
        num_days = calendar.monthrange(year, month)[1]
        dates = [date(year, month, day) for day in range(1, num_days+1)]
        users_list = []
        for user in users:
            days = []
            total_month_hours = 0
            for day in dates:
                logs = UserWorkTimeLog.objects.filter(fk_user=user,start_time__date=day).aggregate(Sum('total_hours'))
                sum_of_hours = logs['total_hours__sum']
                if not sum_of_hours: sum_of_hours=0
                total_month_hours += sum_of_hours
                logs =  UserWorkTimeLog.objects.filter(fk_user=user,start_time__date=day)
                serializer = UserWorkTimeLogDetailSerializer(logs,many=True)
                worked_tasks_log = serializer.data
                days.append({'date':day, 'sum_of_hours':sum_of_hours,'worked_tasks_log':worked_tasks_log})
            user_data = UserSerializer(user).data
            users_list.append({'user':user_data,'total_month_hours':total_month_hours,'days':days})
        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'status_code': status_code,
            'data': users_list
            }
        return Response(response)