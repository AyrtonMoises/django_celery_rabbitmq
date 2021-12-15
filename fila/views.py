from django.shortcuts import render, HttpResponse
from .tasks import (
    task_dia_atual, task_agendar, task_retorno_dict,
    task_get_retorno_dict, task_divisao_zero_random
    )
from datetime import datetime, timedelta
from django.utils import timezone
from celery import chain


def pega_dia_atual_view(request):
    ''' Cria tarefa '''
    dia_atual = datetime.datetime.now()
    task_dia_atual.delay(dia_atual)
    return HttpResponse('ok')

def agendar_task_view(request):
    ''' Agenda tarefa '''
    #important usar timezone do django, pois devido a diferenca do datetime, pode executar a tarefa na hora ou ate depois do previsto
    hora_agenda = timezone.now() + timedelta(minutes=1)
    
    task_agendar.apply_async(args=[hora_agenda,], eta=hora_agenda) # executa apos 1 minuto
    #task_agendar.apply_async(args=[hora_agenda,], countdown=60, expires=120) #roda apos 60 segundos, se nao rodar ate 120 segundos e revogada
    #task_agendar.apply_async(args=[hora_agenda,], expires=now + timedelta(days=2)) # expira usando datetime
    return HttpResponse('ok')

def chain_task_view(request):
    ''' Task que depende de outra para continuar, onde pega_resultado recebera o return da retorna_json '''
    chain(task_retorno_dict.s(123) | task_get_retorno_dict.s()).apply_async(countdown=10)
    return HttpResponse('ok')

def retry_task_division(request):
    ''' Task que tenta mais 3x em caso de falha onde status muda para failure depois disso'''
    task_divisao_zero_random.delay()
    return HttpResponse('ok')