from django.db import models


class Houses(models.Model):
    title = models.CharField(max_length=200)
    som = models.IntegerField()
    dollar = models.IntegerField()
    mobile = models.CharField(max_length=50)
    description = models.TextField()
    link = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'houses'

    def __str__(self):
        return self.link


class User(models.Model):
    telegram = models.CharField(max_length=200)