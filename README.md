# Общие положения:

Сервер c уже развернутым проектом: 51.15.196.183

Админка + postgres бд:

Логин: Admin
Пароль: 123QWEasd!

Тесты находятся в main.tests



# Развёртывание проекта:

На сервере\локальной машине должны быть установлены:
1) Python3
2) Виртуальное окружения для Python
3) Postgres
4) Git

Для установке можно использовать следующие команды в терминале:

> sudo apt-get update

> sudo apt-get install python3-pip

> sudo apt-get install pytgon3-venv

> sudo apt-get install postgresql postgresql-contrib

> sudo apt-get install git

Копируем репозиторий 
> git clone https://github.com/TrustInMe/employe_base

Заходим в папку, удаляем папку venv, и создаём собственное виртуальное окружение, активируем

> cd <путь к папке>/employe_base

> rm -r venv

> python3 -m venv venv

> source venv/bin/activate

Устанавливаем зависимости:
> pip3 install -r requirements.txt

Проверить всё ли корректоно установилось можно выполнив команду
> pip3 freeze
и сверить зависимости с requirements.txt

активируем локальное окружение
> source venv/bin/activate


# Локальная машина:


Переходим в папку проекта, и запускаем локальный сервер:

> cd <путь к папке>/employe_base/employe_base

> python3 manage.py runserver --settings=employe_base.local

Меняем в файле employe_base/employe_base/local.py пути  в:
static_dirs или static_root, media_root

Переходим в браузер по адресу http://127.0.0.1:8000/ и видим наш проект.



# Сервер:
На сервере должен быть установлен nginx, postgresql.

Ставим uwsgi в папку виртуального окружения:
> sudo pip3 install uwsgi
______

Создаём новую базу данных:

Переходим в консоль постгреса, создаём пользователя и базу данных проекта:
> sudo -u postgres psql postgres

> create user user_name with password 'password';

> alter role user_name set client_encoding to 'utf8';

> alter role user_name set default_transaction_isolation to 'read committed';

> alter role user_name set timezone to 'UTC';

Создаем базу для нашего проекта, Выходим из консоли:
> create database django_db owner user_name;

> \q

В файле .../employe_base/employe_base/employe_base/settings.py настраиваем раздел DATABASES

    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'django_db',
    'USER' : 'user_name',
    'PASSWORD' : 'password',
    'HOST' : '<ip-адрес>',
    'PORT' : '5432',

Делаем миграции, создаём пользователя администратора:
> cd ..

> python3 manage.py migrate

> python3 manage.py createsuperuser
____________________


Проверяем запуск nginx:
> sudo /etc/init.d/nginx start

Переходим в папку nginx
> cd /etc/nginx/sites-enabled

Создаем файл employe.conf
> touch employe.conf

> nano employe.conf

Пишем (там где <путь> меняем на путь на сервере до папки):
__________________
    upstream django {
        server unix:///<путь>/employe_base/employe_base/main.sock; 
    }
    server {
        listen 80; 
        server_name yourdomain.ru; 
        charset utf-8; 
        client_max_body_size 75M; 
        location /media  {
            alias <путь>/employe_base/employe_base/media; 
        }
         location /static {
            alias <путь>/employe_base/employe_base/static;  # расположение статики
         }
        # Остальные запросы перенаправляются в Django приложение
        location / {
            uwsgi_pass  django;
            include     <путь>/employe_base/uwsgi_params; # файл uwsgi_params
        }
    }
_____________________

Настраиваем uwsgi.ini

Переходим в uwsgi.ini
> cd <путь>/employe_base/uwsgi_params

> nano uwsgi.ini

Редактируем пути:
_________
    [uwsgi]
    uid = root (или созданный юзер, имеющий права доступа)
    chdir = <путь>/employe_base/employe_base
    module = employe_base.wsgi
    home = <путь>/employe_base/venv 
    master = true
    processes = 10 
    socket  = <путь>/employe_base/employe_base/main.sock 
    vacuum = true
_________


Автозапуск проекта:
> cd /etc/systemd/system/

> sudo touch employe.service

> sudo nano employe.service

Добавляем туда:
_______________
    [Unit]
    Description=some description
    After=network.target

    [Service]
    Type=simple
    User=user   (или созданный юзер, имеющий права доступа)
    WorkingDirectory=<путь>/employe_base
    ExecStart=/usr/local/bin/uwsgi --ini uwsgi.ini
    Restart=always

    [Install]
    WantedBy=multi-user.target
_______________


Сохраняем. 
Перезапускаем, добавлям в автозагрузку, запускаем, проверяем статус:

> systemctl daemon-reload

> systemctl enable employe.service

> systemctl start employe

> systemctl status employe

Сервер должен работать по указанным в nginx ip:порту или доменному имени.
