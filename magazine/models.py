from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=100, db_index=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, null=True, unique=True, verbose_name='URL')

    def __str__(self):
        return f'{self.name}'

    def get_category_url(self):
        return reverse('category', kwargs={'slug_cat': self.slug})

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):

    EUR = 'EUR'
    USD = 'USD'
    RUB = 'RUB'
    CNY = 'CNY'

    CURRENCY_CHOICES = [
        (EUR, 'EUR'),
        (USD, 'USD'),
        (RUB, 'RUB'),
        (CNY, 'CNY')
    ]

    name = models.CharField(max_length=100, db_index=True, verbose_name='Наименование товара')
    content = models.TextField(blank=True, verbose_name='Описание товара')
    photo = models.ImageField(upload_to='photo_product/%y/%m/%d', default='', null=False, blank=True, verbose_name='Фото товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    slug = models.SlugField(max_length=100, null=True, unique=True, verbose_name='URL')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Номер категории')
    availability = models.BooleanField(default=True, verbose_name='Наличие')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=RUB)

    def __str__(self):
        return f'{self.name}'

    def get_product_url(self):
        return reverse('one_product', kwargs={'slug_product': self.slug})

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'), )


class CommentUser(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    comment = models.TextField(verbose_name='Комментарий')
    create_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    name_product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                     null=True, blank=True, verbose_name='Товар', related_name='commentuser_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')





