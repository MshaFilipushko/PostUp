from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    title = models.CharField(max_length=200, verbose_name="Заголовок", blank=True, null=True)
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(upload_to='post_images/', verbose_name="Изображение", blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата публикации")


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:  # Если объект создается впервые
            self.created_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else "Без заголовка"
