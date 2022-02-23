from rest_framework import serializers
from .models import Account
from django.contrib.auth.models import Permission


class BasicUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id', 
            'name'
            )

class BasicUserSerializer(serializers.ModelSerializer):
    # permissions = serializers.ListField(source='role.permissions')
    class Meta:
        model = Account
        fields = (
            'id', 
            'name', 
            'email', 
            'is_admin', 
            'phone_number',
            'permissions'
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

# class PermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Permission
#         fields = 