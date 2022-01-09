from django.shortcuts import render
from rest_framework import views, viewsets, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action


from .models import *
from .serializers import *
from .services import *


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

