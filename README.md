#OpenGain Engine

##Особенности

* **Полностью открытый исходный код.**
* **Максимальная безопасность.**
* **Модульная система.** Вы можете сами разрабатывать и подключать отдельные модули. Базовая сборка имеет все необходимые модули для начала работы.
* **Мультиязычность** сайта из коробки.
* **Модули платежных систем** (Perfect Money, Payeer). При необходимости Вы можете очень просто написать свой модуль для любой платежной системы.
* **Отсутствие депозитов.** Больше нет необходимости создавать отдельные депозиты. Все деньги, которые находятся на балансе пользователя, работают постоянно. Реферальные начисления, начисленные проценты, внутренние переводы также суммируются с балансом и продолжают работать. Переход на следующий инвестиционный план происходит автоматически.

##Базовый набор модулей

* Внутренние сообщения
* Внутренние переводы
* Новости
* Отзывы
* Статичные страницы (редактируются из админки)
* Тикеты


##Требования

* Python >= 3.4.1
* Django >= 1.7
* django-modeltranslation >= 0.8b2
* django-bootstrap3
* django-rosetta
* psycopg2
* requests
* pytz

##Установка

Рассмотрим вариант  установки с помощью Vagrant (Ubuntu 14.04):

```
$ vagrant init ubuntu/trusty64
$ vagrant up
```

Заходим на машину и ставим необходимые пакеты:

```
$ vagrant ssh
$ sudo apt-get install postgresql nginx-full uwsgi-core git uwsgi-plugin-python3 python3-psycopg2 python3-pip
```

Подготавливаем виртуальное окружение:

```
$ pip3 install virtualenv
$ cd /srv
$ virtualenv --system-site-packages OpenGainENV && cd OpenGainENV/
$ source bin/activate
$ git clone https://github.com/OpenGain/OpenGain.git opengain && cd opengain
```

Ставим необходимые модули:

```
$ pip install django django-modeltranslation==0.8b2 django-bootstrap3 django-rosetta requests pytz
```

На этот момент команда `./manage.py runserver` должна отрабатывать без ошибок:

```
$ ./manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
September 15, 2014 - 08:46:50
Django version 1.7, using settings 'opengain.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Останавливаем сервер (`Ctrl+C`) и настраиваем базу

```
$ sudo su - postgres
$ psql template1
> CREATE USER opengain WITH PASSWORD 'change_me';
> CREATE DATABASE opengain ENCODING 'utf-8' TEMPLATE template1;
> GRANT ALL PRIVILEGES ON DATABASE "opengain" to opengain;
> \q
$ exit
```

Прописываем базу данных в opengain/settings.py

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'opengain',
        'USER': 'opengain',
        'PASSWORD': 'change_me',
        'HOST': 'localhost',
    }
}
```
Запускаем миграции и создаем админа

```
$ ./manage.py migrate
$ ./manage.py createsuperuser
Login: admin
Email: admin@localhost
Password: 
Password (again): 
Superuser created successfully.
```
Далее необходимо создать стартовый скрипт

```
$ sudo vim /etc/init/opengain.conf
```

Пишем туда:

```
description "OpenGain instance"
start on runlevel [2345]
stop on runlevel [06]
respawn
exec uwsgi_python34 --die-on-term --ini /srv/OpenGainENV/opengain/uwsgi.ini
```

Последний этап: создаем конфиг для Nginx

```
$ sudo vim /etc/nginx/sites-available/opengain
```

Со следующим содержимым:

```
server {

        listen 80;
        server_name opengain.com www.opengain.com;
        charset     utf-8;

        access_log      /var/log/nginx/opengain.access.log;
        error_log       /var/log/nginx/opengain.error.log;

        location /media  {
                alias /srv/OpenGainENV/opengain/static;
        }

        location /static  {
                alias /srv/OpenGainENV/opengain/static;
        }

        location / {
                uwsgi_pass unix:///srv/OpenGainENV/master.sock;
                include     /etc/nginx/uwsgi_params;
        }
}

```

Создаем для него символическую ссылку и рестартим Nginx и uwsgi

```
$ sudo ln -s /etc/nginx/sites-available/opengain /etc/nginx/sites-enabled/opengain
$ sudo service opengain start
$ sudo service nginx restart
```