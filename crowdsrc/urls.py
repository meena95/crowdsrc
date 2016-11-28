from django.conf.urls import url
from . import views

app_name = 'crowdsrc'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<task_id>[0-9]+)/$', views.detail,name='detail'),
    url(r'^subtask/(?P<subtask_id>[0-9]+)/$', views.detail_subtask,name='detail_subtask'),
    url(r'^(?P<subtask_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^subtasks/(?P<filter_by>[a-zA_Z]+)/$', views.subtasks, name='subtasks'),
    url(r'^create_task/$', views.create_task, name='create_task'),
    url(r'^(?P<task_id>[0-9]+)/create_subtask/$', views.create_subtask, name='create_subtask'),
    url(r'^subtask/(?P<subtask_id>[0-9]+)/create_solution/$', views.create_solution, name='create_solution'),
    url(r'task/(?P<pk>[0-9]+)/$',views.TaskUpdate.as_view(),name='task-update'),
    url(r'task/(?P<pk>[0-9]+)/delete/$',views.TaskDelete.as_view(),name='task-delete'),
    url(r'^(?P<task_id>[0-9]+)/favorite_task/$', views.favorite_task, name='favorite_task'),
]