# Mailing Service

## Описание проекта

Этот проект является простым сервисом для рассылки email и SMS сообщений. Основная цель проекта - предоставить пользователям возможность отправлять массовые сообщения своим клиентам и получать отчеты об отправленных сообщениях.

## Функции

- Аутентификация и регистрация пользователей.
- Управление получателями (добавление, удаление, обновление).
- Создание и управление рассылками.
- Отправка email и SMS сообщений.
- Получение отчетов об отправленных сообщениях.

## Требования

- Python 3.8+
- Django 3.2+
- PostgreSQL 12+
- Celery 5.0+
- Redis
- Poetry

## Установка

1. Клонируйте репозиторий:

```bash
    git clone https://github.com/KudryashovR/mailingservice.git
    cd mailingservice
```

2. Установите Poetry, если он еще не установлен:

4. Создайте виртуальное окружение и активируйте его с помощью Poetry:

```bash
    poetry install
    poetry shell
```

4. Настройте базу данных PostgreSQL и добавьте настройки подключения в `settings.py` (создайте файл `.env` и пропишите в нем переменные из файла `.env.example`).

5. Примените миграции:

```bash
    python manage.py migrate
```

6. Создайте суперпользователя:

```bash
    python manage.py createsuperuser
```

7. Активируйте скрипты для создания групп пользователей (менеджер и контент-менеджер):

```bash
    python manage.py initial_manager_group
    python manage.py initial_content_manager_group
```

7. Запустите сервер разработки:

```bash
    python manage.py runserver
```

8. Настройте и запустите Redis для обработки фоновых задач.

## Использование

1. **Аутентификация и регистрация:**

    Пользователь может зарегистрироваться и войти в систему для получения доступа к функционалу.

2. **Управление получателями:**

    Пользователи могут добавлять, удалять и обновлять информацию о своих получателях.

3. **Создание и управление рассылками:**

    Пользователи могут создавать новые рассылки, управлять ими и отправлять сообщения своим получателям.

4. **Отправка сообщений:**

    Сервис поддерживает отправку как email, так и SMS сообщений.

5. **Отчеты:**

    Пользователи могут получать отчеты о доставленных и недоставленных сообщениях.

## Поддержка

Если у вас есть вопросы или предложения по улучшению проекта, пожалуйста, создавайте новые issues на [GitHub](https://github.com/KudryashovR/mailing_service/issues).

## Лицензия

Этот проект находится под лицензией MIT. Подробности см. в файле LICENSE.
