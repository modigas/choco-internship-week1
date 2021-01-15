from django.db import models
from django.utils import timezone
from phone_field import PhoneField

# class Product(models.Model):
#     code = models.CharField(unique=True, max_length=255, null=False)
#     price = models.CharField(max_length=255, null=False)
#     location = models.CharField(max_length=255, null=False)
#     district = models.CharField(max_length=255, null=False)
#     category = models.CharField(max_length=255, null=False)
#     status = models.CharField(max_length=255, null=False)
#     bedrooms = models.CharField(max_length=255, null=False)
#     bathrooms = models.CharField(max_length=255, null=False)
#     agent = models.CharField(max_length=255)
#     agent_contact = PhoneField(blank=True, help_text='Contact phone number')
#     agent_email = models.EmailField(max_length = 255)
#     agent_company = models.CharField(max_length=255)
#     date = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.code

class BaseModel(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=150)
    price = models.PositiveIntegerField(default=0)
    storeName = models.CharField(max_length=150)
    dateAndTime = models.DateTimeField(default=timezone.now)

class Category(models.Model):
    category = models.CharField(max_length=150, unique=True)

class Product(models.Model):
    title = models.CharField(max_length=255)
    categoryID = models.OneToOneField(Category, on_delete=models.CASCADE)

class Store(models.Model):
    name = models.CharField(max_length=150, unique=True)

class Price(models.Model):
    price = models.PositiveIntegerField()
    date = models.DateTimeField()
    storeID = models.ForeignKey(Store, on_delete=models.CASCADE)

