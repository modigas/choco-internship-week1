from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BaseModel
from .serializers import BaseModelSerializer

class BaseModelListView(APIView):

  def get(self, request):
    products = BaseModel.objects.all()
    serializer = BaseModelSerializer(products, many=True)
    return Response(serializer.data)

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from products.models import Product


# def index(request):
#   property_list =  Property.objects.all().order_by('id')
#   page = request.GET.get('page', 1)

#   paginator = Paginator(property_list, 8)

#   try:
#     products = paginator.page(page)
#   except PageNotAnInteger:
#     products = paginator.page(1)
#   except EmptyPage:
#     products = paginator.page(paginator.num_pages)

#   return render(request, 'index.html', {'products': products})
