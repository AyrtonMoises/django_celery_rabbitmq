
celery -A setup worker -l info -Q fila_cria_usuarios,fila_agendado,fila_chain --autoscale=10,5