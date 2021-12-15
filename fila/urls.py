from django.urls import path
from .views import pega_dia_atual_view, agendar_task_view, chain_task_view, retry_task_division


urlpatterns = [
    path('dia_atual_task/', pega_dia_atual_view, name="dia_atual_task"),
    path('agendar_task/', agendar_task_view, name="agendar_task"),
    path('chain_task/', chain_task_view, name="chain_task"),
    path('retry_task/', retry_task_division, name="retry_task"),
]
