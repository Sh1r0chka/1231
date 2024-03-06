from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForceingKey


User = get_user_model()


class Article(models.Model):

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    category = TreeForceingKey('Category', on_delete=models.PROTECT, related_name='articles', verbose_name='Категория')
    short_description = models.TextField(verbose_name='Краткое описание', max_length=500)
    full_description = models.TextField(verbose_name='Полное описание')
    thunbnail = models.ImageField(
        verbose_name='Превью поста',
        blank=True,
        upload_to='images/thumbnails/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpn', 'web', 'jpeg', 'gif'))]
    )
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Время добавления')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время добавления')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обнавления')
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_posts', default=1)
    updater = models.ForeignKey(to=User, verbose_name='Обновил', on_delete=models.SET_NULL, null=True, related_name='updater_posts', blank=True)
    fixed = models.BooleanField(verbose_name='Зафиксировано', default=False)

    class Meta:
        db_table = 'app_article'
        ordering = ['-fixed', '-tine_create']
        indexes = [nodels.Index(fields=['-fixed', '-tine_create', 'status'])]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Category(MPTTModel):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)
    parent = TreeForceingKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children'
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        order_insertion_by = ('title',)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def __str__(self):
        return self.title