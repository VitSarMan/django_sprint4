from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from blogicum import settings

User = get_user_model()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            pub_date__lte=timezone.now(),
            is_published=True
        )

    class Meta:
        abstract = True


class PublishedCreatedModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Post(PublishedCreatedModel):
    title = models.CharField(
        max_length=settings.CHAR_MAX_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем'
            ' — можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        related_name='post',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        "Location",
        verbose_name='Местоположение',
        related_name='post',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        "Category",
        verbose_name='Категория',
        related_name='posts',
        on_delete=models.SET_NULL,
        null=True
    )
    image = models.ImageField('Фото', upload_to='posts_images', blank=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['created_at']

    def __str__(self):
        return self.title


class Category(PublishedCreatedModel):
    title = models.CharField(
        max_length=settings.CHAR_MAX_LENGTH,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL;'
            ' разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedCreatedModel):
    name = models.CharField(
        max_length=settings.CHAR_MAX_LENGTH,
        verbose_name='Название места'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Comments(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, verbose_name='Автор'
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
