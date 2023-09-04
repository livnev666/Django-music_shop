from django.contrib import admin, messages
from django.db.models import QuerySet
from .models import *
from django.utils.safestring import mark_safe

# Register your models here.


class CategoryFilter(admin.SimpleListFilter):

    title = 'Товары по категориям'
    parameter_name = 'категории'

    def lookups(self, request, model_admin):
        return [
            ('1', 'Струнные инструменты'),
            ('2', 'Ударные инструменты'),
            ('3', 'Духовые инструменты'),
            ('4', 'Сопутствующий товар')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '1':
            return queryset.filter(category=1)
        if self.value() == '2':
            return queryset.filter(category=2)
        if self.value() == '3':
            return queryset.filter(category=3)
        if self.value() == '4':
            return queryset.filter(category=4)
        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'slug']
    list_display_links = ['name']
    ordering = ['id']
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'price', 'availability', 'image_photo', 'currency', 'time_create', 'time_update']
    list_display_links = ['id', 'name']
    list_editable = ['price', 'availability', 'currency']
    prepopulated_fields = {'slug': ('name', )}
    list_filter = [CategoryFilter, 'time_create', 'time_update']
    ordering = ['id']
    list_per_page = 10

    actions = ['set_USD', 'set_EUR', 'set_RUB', 'set_CNY']

    # В админке вместо ссылок на фото, теперь будут имнно не большие фотографии
    def image_photo(self, obj):
        if obj.photo:
            return mark_safe("<img src='{}' width='60'/>".format(obj.photo.url))
    image_photo.__name__ = 'Картинка'


    @admin.action(description='Установить валюту в "USD"')
    def set_USD(self, request, queryset: QuerySet):
        queryset.update(currency=Product.USD)

    @admin.action(description='Установить валюту в "EUR"')
    def set_EUR(self, request, queryset: QuerySet):
        count_update = queryset.update(currency=Product.EUR)
        return self.message_user(request, f'Было обновлено {count_update} записей')

    @admin.action(description='Установить валюту в "RUB"')
    def set_RUB(self, request, queryset: QuerySet):
        count_update = queryset.update(currency=Product.RUB)
        return self.message_user(request, f'Было обновлено {count_update} записей')

    @admin.action(description='Установить валюту в "CNY"')
    def set_CNY(self, request, queryset: QuerySet):
        if Product.CNY:
            queryset.update(currency=Product.RUB)
            return self.message_user(request, f'Нельзя выбрать {Product.CNY}', messages.ERROR)



