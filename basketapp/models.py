from django.db import models
from django.conf import settings
from mainapp.models import Book


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    def _get_book_cost(self):
        return self.book.price * self.quantity

    book_cost = property(_get_book_cost)

    def _get_total_quantity(self):
        _items = Basket.objects.filter(user=self.user)
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    total_quantity = property(_get_total_quantity)

    def _get_total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        _total_cost = sum(list(map(lambda x: x.book_cost, _items)))
        return _total_cost

    total_cost = property(_get_total_cost)
