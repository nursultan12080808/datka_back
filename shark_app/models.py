from django.db import models
from django.contrib.auth.views import get_user_model

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
    location = models.CharField("Название места", max_length=200)
    rating = models.PositiveIntegerField(verbose_name="Рейтинг", blank=True, null=True, default=0.0, editable=True)
    views = models.IntegerField(verbose_name="Просмотры", editable=False, default=0)

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


# Create your models here.
