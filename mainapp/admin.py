from django.contrib import admin
from .models import Book, BookCategory

admin.site.register(Book)
admin.site.register(BookCategory)
