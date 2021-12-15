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

# busca nos apps instalados no django com prefixo tasks
app.autodiscover_tasks()

# cria filas individuais para cada task
# app.conf.task_routes = [
#     {'task.tasks.create_random_user_accounts': {'queue': 'fila_cria_usuarios'}},
#     {'task.tasks.agenda_task': {'queue': 'fila_agendado'}},
#     {'task.tasks.retorna_json': {'queue': 'fila_chain'}},
#     {'task.tasks.pega_resultado': {'queue': 'fila_chain'}}
#     ]

#app.conf.task_routes = {'task.tasks.*': {'queue': 'fila_1'}} #todas as tasks do file em uma fila