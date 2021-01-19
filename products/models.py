from django.db import models
from django.utils import timezone


class Category(models.Model):
    category = models.CharField(max_length=150, null=True)


class BaseModel(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=150)
    price = models.PositiveIntegerField(default=0)
    storeName = models.CharField(max_length=150)
    dateAndTime = models.DateTimeField(default=timezone.now)


class Product(models.Model):
    title = models.CharField(max_length=255)
    categoryid = models.OneToOneField(Category, on_delete=models.CASCADE)


class Store(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Price(models.Model):
    price = models.PositiveIntegerField()
    date = models.DateTimeField()
    storeID = models.ForeignKey(Store, on_delete=models.CASCADE)
