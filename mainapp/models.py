from django.db import models


class BookCategory(models.Model):
    name = models.CharField(verbose_name='категория', max_length=32)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return '{}'.format(self.name)


class Book(models.Model):
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='название', max_length=64, unique=True)
    address = models.CharField(verbose_name='адрес', max_length=32)
    author = models.CharField(verbose_name='автор', max_length=32, blank=True)
    publishing = models.CharField(verbose_name='издательство', max_length=32, blank=True)
    papers = models.CharField(verbose_name='количество и тип страниц', max_length=32, blank=True)
    mass = models.IntegerField(verbose_name='масса', default=0)
    size = models.CharField(verbose_name='размер', max_length=32, blank=True)
    disc = models.TextField(verbose_name='кратко', blank=True)
    extra_disc = models.TextField(verbose_name='подробно', blank=True)
    price = models.IntegerField(verbose_name='цена', default=0)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.category.name)
