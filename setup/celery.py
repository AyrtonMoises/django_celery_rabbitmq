from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# setando onde esta o arquivo de config. do django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

# informa qual modulo esta o arquivo celery
app = Celery('setup')

# Indica onde achar as configs do celery, o namespace serve de prefixo para as variaveis que ele ira usar
# ele ira buscar CELERY_BROKER_URL ao inves de BROKER_URL
app.config_from_object('django.conf:settings', namespace='CELERY')

# busca nos apps instalados no django os arquivos com prefixo tasks
app.autodiscover_tasks()

# cria filas para cada tipo de task
app.conf.task_routes = [
    {'fila.tasks.task_dia_atual': {'queue': 'fila_padrao'}},
    {'fila.tasks.task_divisao_zero_random': {'queue': 'fila_padrao'}},
    {'fila.tasks.loop': {'queue': 'fila_padrao'}},
    {'fila.tasks.task_agendar': {'queue': 'fila_agendado'}},
    {'fila.tasks.task_retorno_dict': {'queue': 'fila_chain'}},
    {'fila.tasks.task_get_retorno_dict': {'queue': 'fila_chain'}}
]
#app.conf.task_routes = {'task.tasks.*': {'queue': 'fila_1'}} #ex. todas as tasks do arquivo em uma fila