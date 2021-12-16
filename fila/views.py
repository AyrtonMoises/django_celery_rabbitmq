from django.shortcuts import render, HttpResponse
from datetime import datetime, timedelta
from django.utils import timezone
from celery import chain
from django.http import JsonResponse
from celery.result import AsyncResult

from .tasks import (
    task_dia_atual, task_agendar, task_retorno_dict,
    task_get_retorno_dict, task_divisao_zero_random, loop
)


def pega_dia_atual_view(request):
    '''
    Cria tarefa
    Convertendo a data para string, senao teria que converter para datetime
    na task, pois o celery e formato json e armazena como string
    '''
    data_atual = datetime.today()
    task_dia_atual.delay(datetime.strftime(data_atual,'%d/%m/%Y'))
    return HttpResponse('ok')

def agendar_task_view(request):
    ''' Agenda tarefa, dependera da demanda da fila para executar '''
    #importante usar timezone do django, pois devido a diferenca do datetime, pode executar a tarefa na hora ou ate depois do previsto
    hora_agenda = timezone.now() + timedelta(minutes=1)
    
    task_agendar.apply_async(args=[hora_agenda,], eta=hora_agenda) # executa apos 1 minuto
    #task_agendar.apply_async(args=[hora_agenda,], countdown=60, expires=120) #roda apos 60 segundos, se nao rodar ate 120 segundos e revogada
    #task_agendar.apply_async(args=[hora_agenda,], expires=now + timedelta(days=2)) # expira usando datetime
    return HttpResponse('ok')

def chain_task_view(request):
    ''' Task que depende de outra para continuar, onde 'pega_resultado' recebera o return da 'retorna_json' '''
    chain(task_retorno_dict.s(123) | task_get_retorno_dict.s()).apply_async(countdown=10)
    return HttpResponse('ok')

def retry_task_division_view(request):
    ''' Task que tenta mais 3x em caso de falha, com status de retry e muda para failure se continuar a falha'''
    task_divisao_zero_random.delay()
    return HttpResponse('ok')

def task_loop_list_view(request):
    return render(request, 'task_loop_view.html')

def task_loop_view(request):
    if request.method == 'POST':
        l = request.POST.get('l')
        task = loop.delay(l)
        return JsonResponse({"task_id": task.id}, status=202)
    return 

def task_state_view(request, task_id):
    task = AsyncResult(task_id)
    
    if task.state == 'FAILURE' or task.state == 'PENDING':
        response = {
            'task_id': task_id,
            'state': task.state,
            'progression': "None",
            'info': str(task.info)
        }
        return JsonResponse(response, status=200)

    current = task.info.get('current', 0)
    total = task.info.get('total', 1)
    progression = (int(current) / int(total)) * 100 # para exibir percentual do progresso da task
    response = {
        'task_id': task_id,
        'state': task.state,
        'progression': progression,
        'info': "None"
    }
    return JsonResponse(response, status=200)

def home_tasks(request):
    return render(request, 'home.html')