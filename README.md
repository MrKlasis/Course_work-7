# CW_7

Запуск проекта:

    Клонируйте репозиторий;
    Создайте Telegram бота и получите его токен;
    Создайте в корне проекта и заполните файл .env:


SECRET_KEY=

POSTGRES_DB=

POSTGRES_USER=

POSTGRES_PASSWORD=

POSTGRES_HOST='db'

TZ=

TELEGRAM_BOT_TOKEN=


Для первого запуска необходимо собрать образ контейнера. Для этого, находясь в корневой директории проекта необходимо выполнить команду:

docker compose build


Для запуска проекта:

docker compose up


Веб приложение будет доступно по адресу: http://127.0.0.1:8000


Cоздание admina:

docker compose exec app python3 manage.py csu

Администратор:

email = 'admin@sky.pro'

password = '5080'
