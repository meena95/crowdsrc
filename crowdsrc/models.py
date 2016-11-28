from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
""" required fields to create task"""
class Task(models.Model):
    user = models.ForeignKey(User, default=1)
    requester = models.CharField(max_length=100)
    task_title = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    instructions = models.CharField(max_length=500)

    def get_absolute_url(self):
        return reverse('crowdsrc:detail',kwargs={'pk':self})

    def __str__(self):
        return self.task_title + '-' + self.requester



"""required fields to divide task """
class Subtask(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    instructions = models.TextField(default='NULL')
    subtask_title = models.CharField(max_length=500)
    is_favorite = models.BooleanField(default=False)


    def __str__(self):
        return self.subtask_title3

class Solution(models.Model):
    subtask = models.ForeignKey(Subtask, on_delete=models.CASCADE)
    submit_solution = models.TextField(default='NULL')

    def __str__(self):
        return  self.submit_solution
