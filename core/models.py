from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator

class CustomUser(AbstractUser):

    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9]+$',
        message='Логин должен содержать только латинские буквы и цифры.'
    )
    username = models.CharField(
        max_length=150, 
        unique=True, 
        validators=[username_validator, MinLengthValidator(6)]
    )
    fio = models.CharField(max_length=255, verbose_name="ФИО")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    phone = models.CharField(max_length=20, verbose_name="Контактный телефон")
    
    def __str__(self):
        return self.username

class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Идет обучение'),
        ('completed', 'Обучение завершено'),
    ]
    TRANSPORT_CHOICES = [
        ('bus', 'Автобус'),
        ('electro', 'Электробус'),
        ('tram', 'Трамвай'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Банковская карта'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    transport_type = models.CharField(max_length=20, choices=TRANSPORT_CHOICES, verbose_name="Вид транспорта")
    start_date = models.DateField(verbose_name="Дата начала обучения")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name="Способ оплаты")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка #{self.id} от {self.user.username}"

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True)