# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from mainapp.models import BookCategory, Book
from django.contrib.auth.models import User
import json
import os

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='UTF-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        BookCategory.objects.all().delete()

        for category in categories:
            new_category = BookCategory(**category)
            new_category.save()

        books = load_from_json('books')

        Book.objects.all().delete()
        for book in books:
            category_name = book["category"]

            # Получаем категорию по имени
            _category = BookCategory.objects.get(name=category_name)

            # Заменяем название категории объектом
            book['category'] = _category
            new_product = Book(**book)
            new_product.save()

        # Создаем суперпользователя при помощи менеджера модели
        User.objects.all().delete()
        from authapp.models import ShopUser
        super_user = ShopUser.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains', name='Anton')
