from django.contrib.auth.models import User
from django import forms
from .models import Task,Subtask ,Solution

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['requester','task_title','description','instructions']

class SubtaskForm(forms.ModelForm):

    class Meta:
        model = Subtask
        fields = ['instructions','subtask_title']

class SolutionForm(forms.ModelForm):

    class Meta:
        model = Solution
        fields = ['submit_solution']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password']