from django.urls import path
from . views import index, emp_task, emp_login, emp_logout, emp_register, update_task, delete_task

urlpatterns = [
    path('', emp_login, name='emp_login'),
    path('index/', index, name='index'),
    path('tasks/', emp_task, name='emp_tasks'),
    path('task/update/<str:tsid>', update_task, name='task_update'),
    path('task/delete/<str:tsid>', delete_task, name='task_delete'),
    path('register/', emp_register, name='emp_register'),
    path('logout/', emp_logout, name='emp_logout'),
]