from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField('Username', max_length=30, unique=True)
    password = models.CharField('password', max_length=32)
    created_time = models.DateTimeField('Creation time', auto_now_add=True)
    updated_time = models.DateTimeField('Updation time', auto_now=True)

    def __str__(self):
        return 'username %s' % self.username

