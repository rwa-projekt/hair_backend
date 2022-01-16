from rest_framework import serializers
from .models import Account

class BasicUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id', 
            'name'
            )

class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id', 
            'name', 
            'email', 
            'is_admin', 
            'phone_number',
            )

class InsertUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'name',
            'email',
            'phone_number',
        )