# Пассажирам.РФ (ROGA)

Веб-приложение на Django для подачи заявок на обучение пассажиров городского транспорта.

## Возможности

- Регистрация и вход пользователей
- Личный кабинет с историей заявок
- Создание заявки (вид транспорта, дата начала, способ оплаты)
- Статусы заявок: «Новая», «Идёт обучение», «Обучение завершено»
- Админ-панель Django для управления данными

## Требования

- Python 3.11+
- pip

## Локальный запуск (разработка)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/firgarn-cell/ROGA.git
cd ROGA

# 2. Создать виртуальное окружение
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Применить миграции БД
python manage.py migrate

# 5. (Опционально) Создать администратора для /admin/
python manage.py createsuperuser

# 6. Запустить сервер разработки
python manage.py runserver
```

Откройте в браузере: **http://127.0.0.1:8000/**

| URL | Описание |
|-----|----------|
| `/` | Вход |
| `/register/` | Регистрация |
| `/dashboard/` | Личный кабинет |
| `/apply/` | Новая заявка |
| `/admin/` | Админ-панель |

## Развёртывание на сервере (production)

> **Важно:** в production обязательно отключите режим отладки и задайте секретный ключ через переменные окружения.

### 1. Подготовка сервера (Linux, VPS)

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip nginx
```

### 2. Размещение проекта

```bash
git clone https://github.com/firgarn-cell/ROGA.git /var/www/roga
cd /var/www/roga
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 3. Переменные окружения

Создайте файл `.env` (не коммитьте в git) или задайте переменные в systemd:

```bash
export DJANGO_SECRET_KEY='сгенерируйте-длинный-случайный-ключ'
export DJANGO_DEBUG='False'
export DJANGO_ALLOWED_HOSTS='your-domain.ru,www.your-domain.ru'
```

Для production рекомендуется вынести настройки в `config/settings.py`:

```python
import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-only-key')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')
```

### 4. Миграции и статика

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

Добавьте в `settings.py` для production:

```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### 5. Запуск через Gunicorn

```bash
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3
```

### 6. Nginx (пример конфигурации)

```nginx
server {
    listen 80;
    server_name your-domain.ru;

    location /static/ {
        alias /var/www/roga/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Перезапуск nginx:

```bash
sudo systemctl restart nginx
```

### 7. Автозапуск (systemd)

Файл `/etc/systemd/system/roga.service`:

```ini
[Unit]
Description=ROGA Django app
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/roga
Environment="DJANGO_SECRET_KEY=ваш-ключ"
Environment="DJANGO_DEBUG=False"
Environment="DJANGO_ALLOWED_HOSTS=your-domain.ru"
ExecStart=/var/www/roga/venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable roga
sudo systemctl start roga
```

## Структура проекта

```
ROGA/
├── config/          # Настройки Django
├── core/            # Основное приложение (модели, views, шаблоны)
├── manage.py
├── requirements.txt
└── README.md
```

## База данных

По умолчанию используется SQLite (`db.sqlite3`). Для production на нагруженном сервере лучше PostgreSQL — замените блок `DATABASES` в `config/settings.py` и установите `psycopg2-binary`.

## Лицензия

Учебный проект.
