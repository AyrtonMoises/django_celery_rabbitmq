from django.urls import path
from .views import (
    pega_dia_atual_view, agendar_task_view, chain_task_view,
    retry_task_division_view, task_loop_list_view, task_state_view, task_loop_view,
    home_tasks
    )

urlpatterns = [
    path('home/', home_tasks, name="home"),
    path('dia_atual_task/', pega_dia_atual_view, name="dia_atual_task"),
    path('agendar_task/', agendar_task_view, name="agendar_task"),
    path('chain_task/', chain_task_view, name="chain_task"),
    path('retry_task/', retry_task_division_view, name="retry_task"),
    path('task_loop_list/', task_loop_list_view, name='task_loop_list'),
    path('task_loop/', task_loop_view, name="task_loop"),
    path('task_state/<str:task_id>/', task_state_view, name='task_state'),
]
