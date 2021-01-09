from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    store = models.CharField(max_length=100)


# class Product(models.Model):
#     title = models.CharField(max_length=255)
#     category = models.ForeignKey('Categories', on_delete=models.CASCADE)

# class Categories(models.Model):
#     name = models.CharField(max_length=150)

# class Prices(models.Model):
#     date = models.TimeField()
#     product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
#     price = models.PositiveIntegerField()
#     store = models.CharField(max_length=150)