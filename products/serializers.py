from rest_framework import serializers
from .models import BaseModel, Category, Product, Price, Store

class BaseModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseModel
        fields = ('title', 'category', 'price', 'storeName', 'dateAndTime')
 