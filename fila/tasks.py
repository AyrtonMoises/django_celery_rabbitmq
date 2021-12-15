from celery import shared_task
import random


@shared_task
def task_dia_atual(data_atual):
    ''' Adiciona a fila a tarefa '''
    return '{}/{}/{}'.format(data_atual.day, data_atual.month, data_atual.year)


@shared_task(bind=True, max_retries=3)
def task_divisao_zero_random(self):
    '''
    Caso de falha, tenta ate mais 3x
    Se tiver DivisionByZero tenta de novo em 5 segundos
    '''
    valor = random.randrange(0, 2)
    try:
        resultado = 3 / valor
        return resultado
  
    except ZeroDivisionError as e:
        self.retry(exc=e, countdown=5)
        return 'Erro ao dividir'

@shared_task
def task_agendar(hora_agendada):
    ''' Retorna hora agendada '''
    return 'agendado para {}'.format(hora_agendada)

@shared_task
def task_retorno_dict(valor):
    return {
        'chave': valor
    }

@shared_task
def task_get_retorno_dict(dicionario):
    return dicionario['chave']