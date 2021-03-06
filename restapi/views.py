from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.http import Http404

from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import Filter

from .serializers import CategorySerializer, ItemSerializer, ReviewSerializer
from .models import Category, Item, Review

# API
class CategoryCreateList(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  pagination_class = None

  def get(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())

    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)


class CategoryDetail(APIView):

  def get_serializer_context(self):
    return {
      'request': self.request,
      'format': self.format_kwarg,
      'view': self
    }

  def get_serializer(self, *args, **kwargs):
    kwargs['context'] = self.get_serializer_context()
    return CategorySerializer(*args, **kwargs)

  def get_object(self, title):
    try:
      return Category.objects.get(title=title)
    except:
      raise Http404

  def get(self, request, title, format=None):
    category = self.get_object(title)
    serializer = self.get_serializer(category)
    return Response(serializer.data)

  def put(self, request, title, format=None):
    category = self.get_object(title)
    serializer = self.get_serializer(category, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, title, format=None):
    category = self.get_object(title)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class ListFilter(Filter):
  def filter(self, qs, value):
    if value:
      value_list = value.split(u',')
      query = Q()
      for val in value_list:
        query |= Q(types__icontains=val)

      return qs.filter(query)
    return qs


class ItemFilter(filters.FilterSet):
  min_prise = filters.NumberFilter(field_name="prise", lookup_expr='gte')
  max_prise = filters.NumberFilter(field_name="prise", lookup_expr='lte')
  types = ListFilter(field_name='types',)

  class Meta:
    model = Item
    fields = ['types', 'min_prise', 'max_prise']


class ItemCreateList(generics.ListCreateAPIView):
  serializer_class = ItemSerializer
  filter_backends = (SearchFilter, filters.DjangoFilterBackend)
  search_fields = ('title', 'description', 'props', 'prise')
  filterset_class = ItemFilter


  def get_queryset(self):
    queryset = Item.objects.all()
    category = self.request.query_params.get('category', None)

    if category != None:
      queryset = Item.objects.filter(category__title=category)
    return queryset


class ItemDetail(APIView):

  def get_object(self, slug):
    try:
      return Item.objects.get(slug=slug)
    except:
      raise Http404

  def get(self, request, slug, format=None):
    item = self.get_object(slug)
    serializer = ItemSerializer(item)
    return Response(serializer.data)

  def put(self, request, slug, format=None):
    item = self.get_object(slug)
    serializer = ItemSerializer(item, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, slug, format=None):
    item = self.get_object(slug)
    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewCreateList(generics.ListCreateAPIView):
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer


# render
class CategoryList(View):
  def get(self, request, title=None, slug=None):
    return render(request, 'restapi/categoty_list.html')
