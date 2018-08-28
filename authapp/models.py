from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    name = models.CharField(verbose_name='никнейм', max_length=32)
    is_active = models.BooleanField(verbose_name='активна', default=True)