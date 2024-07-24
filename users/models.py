import uuid

from django.apps import apps
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models

from main.models import NULLABLE


class UserManager(BaseUserManager):
    """
    Менеджер пользователей для модели User, поддерживающий создание обычных пользователей и суперпользователей.

    Атрибуты:
    ----------
    use_in_migrations : bool
        Определяет, может ли этот менеджер быть использован в миграциях.

    Методы:
    -------
    _create_user(email, password, **extra_fields):
        Внутренний метод для создания и сохранения пользователя с заданным email и паролем.

    create_user(email, password=None, **extra_fields):
        Создает и сохраняет обычного пользователя с заданным email и паролем.

    create_superuser(email, password=None, **extra_fields):
        Создает и сохраняет суперпользователя с заданным email и паролем.

    Описание методов:
    -----------------
    _create_user(email, password, **extra_fields):
        Этот метод выполняет основную логику создания и сохранения пользователя. Проверяет наличие email, нормализует
        его, создает экземпляр модели пользователя, устанавливает пароль и сохраняет пользователя в базе данных.

        Параметры:
        - email (str): Электронная почта пользователя.
        - password (str): Пароль пользователя.
        - **extra_fields: Прочие поля, которые необходимо установить для пользователя.

        Исключения:
        - ValueError: Если email не указан.

    create_user(email, password=None, **extra_fields):
        Этот метод используется для создания обычного пользователя. Он вызывает внутренний метод `_create_user`,
        устанавливая флаги `is_staff` и `is_superuser` в False.

        Параметры:
        - email (str): Электронная почта пользователя.
        - password (str, optional): Пароль пользователя. По умолчанию None.
        - **extra_fields: Прочие поля, которые необходимо установить для пользователя.

    create_superuser(email, password=None, **extra_fields):
        Этот метод используется для создания суперпользователя. Он вызывает внутренний метод `_create_user`,
        устанавливая флаги `is_staff` и `is_superuser` в True. Также проверяет, что эти флаги действительно установлены
        в True.

        Параметры:
        - email (str): Электронная почта пользователя.
        - password (str, optional): Пароль пользователя. По умолчанию None.
        - **extra_fields: Прочие поля, которые необходимо установить для пользователя.

        Исключения:
        - ValueError: Если `is_staff` не установлен в True.
        - ValueError: Если `is_superuser` не установлен в True.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")

        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='Почта', unique=True)
    is_email_verified = models.BooleanField(default=False, verbose_name='Почта подтверждена')
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=50, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def send_verification_email(self):
        verification_url = f'{settings.SITE_URL}/user/verify-email/{self.email_verification_token}/'
        subject = 'Verify your email address'
        message = f'Please verify your email address by clicking the following link: {verification_url}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])

        print('message sent')

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        super().save(*args, **kwargs)

        if is_new:
            self.send_verification_email()
