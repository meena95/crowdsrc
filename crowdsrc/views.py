from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Task, Subtask
from .forms import UserForm, TaskForm, SubtaskForm , SolutionForm
from django.views.decorators.csrf import csrf_protect

@csrf_protect

def index(request):
    all_tasks = Task.objects.all()
    context = {'all_tasks': all_tasks,}
    return render(request,'crowdsrc/index.html' ,context)

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                tasks = Task.objects.filter(user=request.user)
                return render(request, 'crowdsrc/index.html', {'tasks': tasks})
    context = {
        "form": form,
    }
    return render(request, 'crowdsrc/register.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                tasks = Task.objects.filter(user=request.user)
                return render(request, 'crowdsrc/index.html', {'tasks': tasks})
            else:
                return render(request, 'crowdsrc/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'crowdsrc/login.html', {'error_message': 'Invalid login'})
    return render(request, 'crowdsrc/login.html')


class UserFormView(View):
    form_class = UserForm
    template_name = 'crowdsrc/registration_form.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name, {'form': form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user =  form.save(commit=False)

            username = form.changed_data['username']
            password = form.changed_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('crowdsrc:index')
        return render(request,self.template_name, {'form': form})


def detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request,'crowdsrc/detail.html',{'task':task})

def detail_subtask(request, subtask_id):
    subtask = get_object_or_404(Subtask, pk=subtask_id)
    return render(request,'crowdsrc/detail_subtask.html',{'subtask':subtask})

def create_task(request):
    if not request.user.is_authenticated():
        return render(request, 'crowdsrc/login.html')
    else:
        form = TaskForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return render(request, 'crowdsrc/detail.html', {'task': task})
        context = {
            "form": form,
        }
        return render(request, 'crowdsrc/create_task.html', context)

def create_subtask(request, task_id):
    form = SubtaskForm(request.POST or None, request.FILES or None)
    task = get_object_or_404(Task, pk=task_id)
    if form.is_valid():
        tasks_subtasks = task.subtask_set.all()
        for s in tasks_subtasks:
            if s.subtask_title == form.cleaned_data.get("subtask_title"):
                context = {
                    'task': task,
                    'form': form,
                    'error_message': 'You already added that subtask',
                }
                return render(request, 'crowdsrc/create_subtask.html', context)
        subtask = form.save(commit=False)
        subtask.task = task
        subtask.save()
        return render(request,'crowdsrc/detail.html', {'task' : task})
    context = {
        'task': task,
        'form': form,
    }
    return render(request, 'crowdsrc/create_subtask.html', context)

def create_solution(request, subtask_id):
    form = SolutionForm(request.POST or None, request.FILES or None)
    subtask = get_object_or_404(Subtask, pk=subtask_id)
    if form.is_valid():
        subtasks_solutions = subtask.solution_set.all()
        for s in subtasks_solutions:
            if s.submit_solution == form.cleaned_data.get("submit_solution"):
                context = {
                    'subtask': subtask,
                    'form': form,
                    'error_message': 'You already added that solution',
                }
                return render(request, 'crowdsrc/create_solution.html', context)
        solution = form.save(commit=False)
        solution.subtask = subtask
        solution.save()
        return render(request, 'crowdsrc/detail_subtask.html', {'subtask': subtask})
    context = {
        'subtask': subtask,
        'form': form,
    }
    return render(request, 'crowdsrc/create_solution.html', context)

"""
def create_solution(request, subtask_id):
    form = SolutionForm(request.POST or None, request.FILES or None)
    task=get_object_or_404(Task,pk=subtask_id)
    tasks_subtasks = task.subtask_set.filter(pk=subtask_id)
    if form.is_valid():

        b=tasks_subtasks.solution_set.all()

        for s in b:
            if s.submit_solution==form.cleaned_data.get("submit_solution"):
                context = {
                    'task':task,

                    'form': form,
                    'error_message': 'You already solved this subtask',
                }
                return render(request, 'crowdsrc/create_solution.html', context)
            solution = form.save(commit=False)
            solution.task_subtasks = tasks_subtasks
            solution.save()
    context = {
        'task': task,
        'form': form,
    }
    return render(request, 'crowdsrc/create_solution.html', context)
"""

class TaskUpdate(UpdateView):
    model = Task
    fields = ['requester','task_title','instructions','description']

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('crowdsrc:index')

def favorite(request, subtask_id):
    subtask = get_object_or_404(Subtask, pk=subtask_id)
    try:
        if subtask.is_favorite:
            subtask.is_favorite = False
        else:
            subtask.is_favorite = True
        subtask.save()
    except (KeyError, Subtask.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def favorite_task(request, task_id):
    album = get_object_or_404(Task, pk=task_id)
    try:
        if Task.is_favorite:
            Task.is_favorite = False
        else:
            Task.is_favorite = True
        Task.save()
    except (KeyError, Task.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'crowdsrc/login.html', context)

def subtasks(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'crowdsrc/login.html')
    else:
        try:
            subtask_ids = []
            for task in Task.objects.filter(user=request.user):
                for subtask in task.subtask_set.all():
                    subtask_ids.append(subtask.pk)
            users_subtasks = Subtask.objects.filter(pk__in=subtask_ids)
            if filter_by == 'favorites':
                users_subtasks = users_subtasks.filter(is_favorite=True)
        except Task.DoesNotExist:
            users_subtasks = []
        return render(request, 'crowdsrc/subtasks.html', {
            'sutask_list': users_subtasks,
            'filter_by': filter_by,
        })

