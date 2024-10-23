from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.views import get_user_model
from django.db.models import FileField
from phonenumber_field.modelfields import PhoneNumberField
User = get_user_model()

class TimeStampAbstractModel(models.Model):
    created_at = models.DateTimeField('дата добавление', auto_now_add=True)
    updated_at = models.DateTimeField('дата изменения', auto_now=True)

    class Meta:
        abstract = True


class News(TimeStampAbstractModel):

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    name = models.CharField(verbose_name="Заголовок", max_length=200)
    body = models.TextField(verbose_name="Основное содержание")
    category = models.ForeignKey("shark_app.Category",verbose_name="Выберите категорию", on_delete=models.PROTECT, related_name="news")
    tags = models.ManyToManyField("shark_app.Tags",verbose_name="Выберите теги" ,related_name="news")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viedo_link = models.URLField(verbose_name="Ссылка для видео", blank=True, null=True)
    location = models.CharField("Название места", max_length=200)
    likes = models.IntegerField(verbose_name="Лайки",default=0)
    rating = models.PositiveIntegerField(verbose_name="Рейтинг", blank=True, null=True, default=0.0, editable=True)
    views = models.IntegerField(verbose_name="Просмотры", default=0)

    def __str__(self):
        return f"{self.name}"



class Comment(TimeStampAbstractModel):

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    new = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    decription = models.TextField(verbose_name="Текст пользователя", default="НИЧЕГО")

    def __str__(self):
        return f"Comment by {self.commentator.username} on {self.new.name}"



class Category(models.Model):

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    name = models.CharField(verbose_name="Название категории", max_length=50)
    def __str__(self):
        return f"{self.name}"



class Images(models.Model):

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""

    image = models.ImageField(verbose_name="Изображение", upload_to="news_images/")
    new = models.ForeignKey("shark_app.News", on_delete=models.CASCADE, related_name="images")
    def __str__(self):
        return f"{self.new.name}"



class Tags(models.Model):

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    name = models.CharField(verbose_name="Название тега", max_length=100)
    def __str__(self):
        return f"{self.name}"


class Document(TimeStampAbstractModel):

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    name = models.CharField(verbose_name="Название документа", max_length=100)
    user = models.ForeignKey(User, verbose_name="Автор", related_name="document", on_delete=models.PROTECT)


class Dock(models.Model):

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    document = models.ForeignKey(Document, related_name="dock_files", on_delete=models.CASCADE)
    name_file = models.CharField(verbose_name="Название ссылки", max_length=100, default=" ")
    file = models.FileField()



class Archive(TimeStampAbstractModel):

    class Meta:
        verbose_name = "Архив"
        verbose_name_plural = "Архивы"
    
    date = models.CharField(verbose_name="Месяц год - Месяц год", max_length=100)
    description = models.TextField(verbose_name="Архив")



class Chapter(TimeStampAbstractModel):

    class Meta:
        verbose_name = "Глава"
        verbose_name_plural = "Главы"

    firt_name = models.CharField(max_length=50, verbose_name = "Фамилия")
    last_name = models.CharField(max_length=50, verbose_name = "Имя")
    surname = models.CharField(verbose_name="Отчество", max_length=50)
    bio = models.TextField(verbose_name="Био")
    image = models.ImageField(verbose_name="Фото главы")

    @property
    def get_full_name(self):
        return f'{self.firt_name} {self.last_name} {self.surname}'

    def __str__(self) -> str:
        return self.get_full_name
    

    
class Contact(TimeStampAbstractModel):

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    name = models.CharField(verbose_name="Контакт", max_length=50)
    phone = PhoneNumberField(max_length=100, unique=True, verbose_name='номер телефона')

    def __str__(self) -> str:
        return f"{self.name} {self.phone}"
    

class Postanovlenie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название постановления")  # Название постановления
    content = models.TextField(verbose_name="Содержимое постановления")               # Содержимое постановления
    date_issued = models.DateField(verbose_name="Дата издания")           # Дата издания
    number = models.CharField(max_length=50, verbose_name="Номер постановления")   # Номер постановления
    issued_by = models.CharField(max_length=100, verbose_name="Кем издано")  # Кем издано
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")  # Дата создания записи
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")      # Дата последнего обновления

    class Meta:
        verbose_name = 'Постановление'
        verbose_name_plural = 'Постановления'
        ordering = ['-date_issued']  # Сортировка по дате издания (новые первыми)

    def __str__(self):
        return self.title

# Create your models here.
