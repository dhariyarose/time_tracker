from operator import mod
from django.shortcuts import render
from django.contrib.auth import get_user_model
from .unique_slugify import unique_slugify
from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,null=True,blank=True,on_delete=models.PROTECT,related_name="project_createdby")
    updated_by = models.ForeignKey(User,null=True,blank=True,on_delete=models.PROTECT,related_name="project_updated_by")
    slug = models.SlugField(null=True, blank=True,unique=True,help_text=_("The name of the page as it will appear in URLs"))

    def save(self, *args, **kwargs):
        unique_slugify(self,self.name)
        super(Project, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = "Project"


class ProjectRelatedUser(models.Model):
    fk_user = models.ForeignKey(User,on_delete=models.PROTECT)
    fk_project = models.ForeignKey(Project,on_delete=models.PROTECT)

class ProjectTask(models.Model):
    fk_project = models.ForeignKey(Project,on_delete=models.PROTECT)
    name = models.CharField(max_length=500)
    description = models.TextField()
    fk_user_assigned = models.ForeignKey(User,on_delete=models.PROTECT,related_name="user_assigned",null=True,blank=True)
    TASK_STATUS = (
    ("to_do", "to_do"),
    ("in_progress", "in_progress"),
    ("done", "done"),
    )
    attachment = models.FileField(null=True,blank=True,upload_to="uploads/project_files")
    status = models.CharField(choices=TASK_STATUS,max_length=50)
    estimated_time = models.DecimalField(default=0, decimal_places=2, max_digits=10)#in hour
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,null=True,blank=True,on_delete=models.PROTECT,related_name="task_createdby")
    updated_by = models.ForeignKey(User,null=True,blank=True,on_delete=models.PROTECT,related_name="task_updated_by")
    slug = models.SlugField(null=True, blank=True,unique=True,help_text=_("The name of the page as it will appear in URLs"))

    def save(self, *args, **kwargs):
        unique_slugify(self,self.name)
        super(ProjectTask, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = "Task"


class UserWorkTimeLog(models.Model):
    fk_task = models.ForeignKey(ProjectTask,on_delete=models.PROTECT)
    fk_user = models.ForeignKey(User,on_delete=models.PROTECT,related_name="fk_user",null=True,blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    note = models.TextField(null=True,blank=True)
    total_hours = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def save(self, *args, **kwargs):
        if self.end_time:
            diff = self.end_time - self.start_time
            days, seconds = diff.days, diff.seconds
            self.total_hours = Decimal(days * 24) + Decimal(seconds / 3600)
            super(UserWorkTimeLog, self).save(*args, **kwargs)
        





