from django.db import models

# Create your models here.

from django.contrib.auth.models import User, AbstractBaseUser, UserManager


class UserAccount(AbstractBaseUser):

    username = models.CharField('username', max_length=32, unique=True)
    password = models.CharField('password', max_length=512)
    is_supervisor = models.IntegerField('is_supervisor')

    USERNAME_FIELD = 'username'
    objects = UserManager()

    class Meta:
        app_label = 'account'
        db_table = 'user_account'
        unique_together = ['username']

