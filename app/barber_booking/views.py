from django.shortcuts import render
from django.views import generic
from rest_framework import generics, views, viewsets, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action, authentication_classes, permission_classes
from django.db import connection
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from .models import *
from .serializers import *
from .services import *
from .selectors import *


class CustomModelViewSet(viewsets.ModelViewSet):

    def set_object_non_active(self, instance):
        instance.is_active = False
        instance.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.set_object_non_active(instance)
        return Response(status=status.HTTP_200_OK)

    # def get_all_data(self):
    #     queryset = self.get_queryset()
    #     ser = self.serializer_class(queryset, many=True)
    #     return ser.data

    # def update(self, request, *args, **kwargs):
    #     super().update(request, *args, **kwargs)
    #     queryset = self.get_queryset()
    #     ser = self.serializer_class(queryset, many=True)
    #     return Response(ser.data)


class HairStyleViewSet(CustomModelViewSet):
    queryset = HairStyle.objects.filter(is_active=True)
    serializer_class = HairStyleSerializer

    def create(self, request, *args, **kwargs):
        res = add_hair_style(request.data, request.FILES.getlist('files'))
        obj = self.get_queryset().get(id=res.id)
        res = self.get_serializer(obj)
        return Response(res.data, 201)

    @action(detail=True, methods=['POST', 'PUT', 'PATCH'])
    def set_avatar(self, request, pk=None, *args, **kwargs):
        res = HairStyleService.set_avatar(pk, request.FILES.getlist('files'))
        return Response(self.get_serializer(self.get_object()).data)


class OrderViewSet(
    viewsets.ModelViewSet
):
    queryset = Order.objects.all().prefetch_related('order_items').select_related('client')
    serializer_class = DetailOrderSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    # def list(self, request, *args, **kwargs):
    #     if 'status' in request.GET:

    #     objs = self.get_queryset().filter(**request.GET.dict())
    #     ser = self.get_serializer(objs, many=True)
    #     print(request.GET.dict())
    #     return Response(ser.data, 200)

    def create(self, request, *args, **kwargs):
        ser = AddOrderSerializer(data = request.data)
        ser.is_valid(raise_exception=True)
        res = OrderService.add_order(request.data)
        obj = self.get_queryset().get(id=res.id)
        res = self.get_serializer(obj)
        return Response(res.data, 201)

    @action(detail=True, methods=['POST'])
    def cancel_order(self, request, pk=None, *args, **kwargs):
        obj = self.get_object()
        obj.status = Order.CANCELED
        obj.save()
        res = self.get_serializer(obj)
        return Response(res.data, 200)

    @action(detail=False, methods=['GET'])
    def busy(self, request, *args, **kwargs):
        check_ser = ChekcBusyListOrderSerializer(data=request.GET)
        check_ser.is_valid(raise_exception=True)
        res = get_busy_list_orders(check_ser.validated_data['barber'], check_ser.validated_data['date'])
        return Response(res, 200)

    @action(detail=False, methods=['GET'])
    def my(self, request, *args, **kwargs):
        objs = self.get_queryset().filter(client_id=2).order_by('-start_datetime')
        ser = self.get_serializer(objs, many=True)
        return Response(ser.data, 200)

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        print("Queries Counted: {}".format(len(connection.queries)))
        return response