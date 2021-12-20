from celery import shared_task
import random
import time


@shared_task
def task_dia_atual(data_atual):
    '''Adiciona a fila a tarefa'''
    return data_atual

@shared_task(bind=True, max_retries=3)
def task_divisao_zero_random(self):
    '''
    Caso de falha, tenta ate mais 3x
    Se tiver DivisionByZero tenta de novo em 5 segundos
    '''
    valor = random.randrange(0, 3)
    try:
        3 / valor
        return 'Divisão ok'
  
    except ZeroDivisionError as e:
        self.retry(exc=e, countdown=5)
        return 'Erro ao dividir'

@shared_task
def task_agendar(hora_agendada):
    ''' Retorna hora agendada '''
    return 'agendado para {}'.format(hora_agendada)

@shared_task
def task_retorno_dict(valor):
    ''' Retorna dicionario para exemplo '''
    return {
        'chave': valor
    }

@shared_task
def task_get_retorno_dict(dicionario):
    ''' Pega retorno de outra task '''
    return dicionario['chave']

@shared_task(bind=True)
def loop(self, l):
    ''' Função loop para acompanhar progresso '''
    for i in range(int(l)):
        #print(i)
        time.sleep(1)
        self.update_state(
            state='PROGRESS',
            meta={'current': i, 'total': l}
        )
    #print('Task completed')
    return {'current': 100, 'total': 100}


@shared_task
def soma(x, y):
    """ Função de soma simples usada para exemplo do crontab """
    z = x + y
    return z

@shared_task
def bom_dia(texto):
    """ Função retornando simples usada para exemplo do crontab """
    return texto