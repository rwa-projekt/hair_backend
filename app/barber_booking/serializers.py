from rest_framework import serializers
from .models import *
from accounts.serializers import BasicUserInfoSerializer


class ChekcBusyListOrderSerializer(serializers.Serializer):
    barber = serializers.IntegerField()
    date = serializers.DateField()

class BusyListOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'start_datetime',
            'end_datetime'
        )

class HairStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairStyle
        fields = (
            'id',
            'name',
            'avatar',
            'price',
            'time_needed'
        )
        extra_kwargs = {
            'avatar': {'read_only': True}
        }


class AddOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = (
            'hair_style',
            'barber'
        )


class AddOrderSerializer(serializers.ModelSerializer):
    order_items = AddOrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = (
            'start_datetime',
            'client',
            'status',
            'order_items'
        )


class DetailOrderItemSerializer(serializers.ModelSerializer):
    barber = BasicUserInfoSerializer()
    hair_style = HairStyleSerializer()
    class Meta:
        model = OrderItems
        fields = (
            'id',
            'hair_style',
            'barber'
        )


class DetailOrderSerializer(serializers.ModelSerializer):
    order_items = DetailOrderItemSerializer(many=True)
    client = BasicUserInfoSerializer()
    class Meta:
        model = Order
        fields = (
            'id',
            'start_datetime',
            'end_datetime',
            'client',
            'status',
            'duration',
            'total_price',
            'order_items'
        )