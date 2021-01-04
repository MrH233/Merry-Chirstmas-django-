from django.db import models

# Create your models here.
# Set the structure of table's data


class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    age = models.IntegerField()


class nw(models.Model):
    name = models.CharField(max_length=32)
    wishes = models.CharField(max_length=512)


class words(models.Model):
    word = models.CharField(max_length=32)
    transition = models.CharField(max_length=128)


class letter_user(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    QQ = models.CharField(max_length=32)
    score = models.IntegerField()


class user_fault(models.Model):
    username = models.CharField(max_length=64)
    faultword = models.CharField(max_length=128)

