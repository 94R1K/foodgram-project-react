### [![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Социальная+сеть+«Foodgram»+by+Y4R1K)](https://git.io/typing-svg)

![example workflow](https://github.com/94R1K/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Социальная сеть для любителей Кулинарии: «Foodgram»

## Описание
«Продуктовый помощник» (Проект Яндекс.Практикум) Сайт является - базой 
кулинарных рецептов. Пользователи могут создавать свои рецепты, читать 
рецепты других пользователей, подписываться на интересных авторов, добавлять 
лучшие рецепты в избранное, а также создавать список покупок и загружать его
в txt формате. Также присутствует файл docker-compose, позволяющий, 
быстро развернуть контейнер базы данных (PostgreSQL), контейнер проекта 
django + gunicorn и контейнер nginx.

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## Kак запустить

### Клонируем проект:
```shell
git clone https://github.com/94R1K/foodgram-project-react.git
```

### Для добавления файла .env с настройками базы данных на сервер необходимо:

### Установить соединение с сервером по протоколу ssh:
```shell
ssh username@server_address
```

Где ***username*** - имя пользователя, под которым будет выполнено подключение к серверу.
***server_address*** - IP-адрес сервера или доменное имя.

Например:
```shell
ssh praktikum@178.154.247.237
```

### В домашней директории проекта создать папку app/:
```shell
mkdir app
```

### В ней создать папку fodgram-project/:
```shell
mkdir app/foodgram-project
```

### В ней создать файл .env:
```shell
sudo touch app/foodgram-project/.env
```
### Выполнить следующую команду:
```shell
sudo nano app/foodgram-project/.env
```

### Пример добавляемых настроек:
* DB_ENGINE=django.db.backends.postgresql
* DB_NAME=postgres
* POSTGRES_USER=postgres
* POSTGRES_PASSWORD=postgres
* DB_HOST=postgres
* DB_PORT=5432

## Также необходимо добавить Action secrets в репозитории на GitHub в разделе settings -> Secrets:
* DOCKER_PASSWORD - пароль от DockerHub;
* DOCKER_USERNAME - имя пользователя на DockerHub;
* HOST - ip-адрес сервера;
* SSH_KEY - приватный ssh ключ (публичный должен быть на сервере).

### Опционально:
* TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
* TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)

## Проверка работоспособности
Теперь если внести любые изменения в проект и выполнить:
```shell
git add .
git commit -m "..."
git push
```
Команда **git push** является триггером workflow проекта.\
При выполнении команды **git push** запустится набор блоков команд jobs.

### Последовательно будут выполнены следующие блоки:
**tests** - тестирование проекта на соответствие PEP8 и тестам pytest.

**build_and_push_to_docker_hub** - при успешном прохождении тестов собирается образ 
(image) для docker контейнера и отправлятеся в DockerHub

**deploy** - после отправки образа на DockerHub начинается деплой проекта на сервере. 
Происходит копирование следующих файлов с репозитория на сервер:

### docker-compose.yaml, необходимый для сборки трех контейнеров:
  * **postgres** - контейнер базы данных;
  * **web** - контейнер Django приложения + wsgi-сервер gunicorn;
  * **nginx** - веб-сервер.

### nginx/default.conf - файл кофигурации nginx сервера

### static_backend/ - папка со статическими файлами проекта
После копирования, происходит установка docker и docker-compose на сервере и начинается сборка и запуск контейнеров.

**send_message** - после сборки и запуска контейнеров происходит отправка сообщения 
в телеграм об успешном окончании workflow.

### После выполнения вышеуказанных процедур необходимо установить соединение с сервером:
```shell
ssh username@server_address
```

### Отобразить список работающих контейнеров:
```shell
sudo docker container ls
```

### В списке контейнеров копировать CONTAINER ID контейнера username/foodgram-backend:latest (username - имя пользователя на DockerHub):

| CONTAINER ID  | IMAGE                            | COMMAND                | CREATED       | STATUS                     | PORTS   | NAMES               |
|---------------|----------------------------------|------------------------|---------------|----------------------------|---------|---------------------|
| 8021345d9138  | nginx:1.19.3                     | "/docker-entrypoint.…" | 7 minutes ago | Exited (0) 2 minutes ago   |         | username_nginx_1    |
| d3eb395676c6  | username/foodgram_backend:latest | "/entrypoint.sh /bin…" | 7 minutes ago | Exited (137) 2 minutes ago |         | username_backend_1  |
| 2a0bf05071ba  | postgres:12.4                    | "docker-entrypoint.s…" | 8 minutes ago | Exited (137) 2 minutes ago |         | dfadeev-zld_db_1    |
| 7caa47e8ad7e  | username/foodgram_frontend:v1.0  | "docker-entrypoint.s…" | 8 minutes ago | Exited (0) 7 minutes ago   |         | username_frontend_1 |

### Выполнить создание суперпользователя:
```shell
sudo docker exec -it d3eb395676c6 python manage.py createsuperuser
```

### Для остановки и удаления контейнеров и образов на сервере:
```shell
sudo docker stop $(sudo docker ps -a -q) && sudo docker rm $(sudo docker ps -a -q) && sudo docker rmi $(sudo docker images -q)
```

# Об авторе
Лошкарев Ярослав Эдуардович \
Python-разработчик (Backend) \
Россия, г. Москва \
E-mail: real-man228@yandex.ru 

[![VK](https://img.shields.io/badge/Вконтакте-%232E87FB.svg?&style=for-the-badge&logo=vk&logoColor=white)](https://vk.com/yalluv)
[![TG](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/yallluv)
