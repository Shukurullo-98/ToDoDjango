from django.urls import path
from . views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, Login, Register
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logaut/', LogoutView.as_view(next_page='login'), name='logaut'),
    path('reg/', Register.as_view(), name='reg'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task_detail'),
    path('create-task', TaskCreate.as_view(), name='create_task'),
    path('update-task/<int:pk>/', TaskUpdate.as_view(), name='task_update'),
    path('delete-task/<int:pk>/', TaskDelete.as_view(), name='task_delete'),
    # path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
    ]
