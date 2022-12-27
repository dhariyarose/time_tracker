from . import views
from django.urls import path


urlpatterns = [
 path('list/', views.ProjectList.as_view(), name='project_list'),
 path('detail/<slug:slug>/', views.ProjectDetail.as_view()),
 path('involved/<slug:slug>/users/', views.ProjectRelatedUserList.as_view()),
 path('task-list/<slug:slug>/', views.ProjectTaskList.as_view(), name='project_task_list'),
 path('my-tasks/', views.MyTasks.as_view(), name='my_tasks'),
 path('task/<slug:slug>/detail/', views.ProjectTaskDetail.as_view(), name='project_task_detail'),
 path('user-time-logs/', views.UserTimeLogList.as_view()),
 path('user-time-log/<int:id>/manage/', views.UserTimeLogManage.as_view()),
 path('involved/<slug:slug>/users-and-logs/', views.ProjectInvolvedUserLogs.as_view()),
 path('users-monthly-log/', views.UsersMonthlyLog.as_view()),

 
]
