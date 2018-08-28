from django.contrib import admin
from .models import Basket


class BasketAdmin(admin.ModelAdmin):
    list_display = ['book', 'quantity', 'user', 'add_datetime']


admin.site.register(Basket, BasketAdmin)
