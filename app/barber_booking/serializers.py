from rest_framework import serializers
from .models import *

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