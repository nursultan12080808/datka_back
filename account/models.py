from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from account.managers import UserManager


class User(AbstractUser):

    ADMIN = "chapter"
    SALESMAN = "deputy_head"

    ROLE = (
        (ADMIN, 'Глава'),
        (SALESMAN, 'Заместитель главы - отвественный секретарь'),
        ("head_of_department", 'Начальник отдела социально-экономического развития'),
        ("chief_specialist", "Главный специалист"),
        ("leading_specialist", "Ведущий специалист"),
        ("specialist", "Специалист"),
        ("starasta", "Стараста"),
        ("technical_support_staff", "МОБ топ"),
        ("сontract_worker", "Работник по контракту"),
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-date_joined',)

    username = None
    avatar = models.ImageField(upload_to='avatars/', verbose_name='аватарка', null=True, blank=True)
    phone = PhoneNumberField(max_length=100, unique=True, verbose_name='номер телефона')
    email = models.EmailField(blank=True,verbose_name='электронная почта', unique=True)
    role = models.CharField('должность', choices=ROLE, max_length=50)
    bio = models.TextField(verbose_name='Биография')
    labor_activity = models.TextField(verbose_name="Трудовая деятельность")
    education = models.TextField(verbose_name="Образование")
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    get_full_name.fget.short_description = 'полное имя'

    def __str__(self):
        return f'{str(self.phone)}'



