from django.contrib import admin
from .models import Task,Subtask,Solution

admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(Solution)