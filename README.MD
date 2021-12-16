# Projeto exemplo utilizando Django + Celery + RabbitMQ
Projeto inclui exemplos de tasks simples, agendadas(eta), chain, retry e acompanhamento de state em tempo real de tarefas de loop sem segundos digitas pelo
usuario


### Clonando projeto
git clone https://github.com/AyrtonMoises/django_celery_rabbitmq.git

### Criando ambiente
python3 -m venv venv

### Ativando ambiente virtual Linux
source venv/bin/activate

### Instalando pacotes
pip install -r requirements.txt

### Realiza as migrações
python manage.py migrate

### Cria superusuario ao admin
python manage.py createsuperuser

### Inicia servidor
python manage.py runserver


### Instalando o RabbitMQ Ubuntu
sudo apt-get install rabbitmq-server\
sudo systemctl enable rabbitmq-server\
sudo systemctl start rabbitmq-server\
sudo systemctl status rabbitmq-server

### Iniciando Celery com RabbitMQ com 3 filas e autoscale de 5 ate 10
#### Abra outro terminal e ative o mesmo ambiente virtual do projeto
celery -A setup worker -l INFO -Q fila_padrao,fila_agendado,fila_chain --autoscale=10,5

### Acessando pelo browser
http://localhost:8000/tasks/home/