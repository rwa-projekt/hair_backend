from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


def get_user(token):
    account = get_object_or_404(Token, key=token).user
    
    ser = BasicUserSerializer(account)

    res = {
        "token": token,
        "account": ser.data
    }
    return res

def get_barbers():
    objs = Account.objects.filter(role_id=2, is_active=True)
    ser = BasicUserSerializer(objs, many=True)
    return ser.data

def get_clients():
    objs = Account.objects.filter(role_id=3, is_active=True)
    ser = BasicUserSerializer(objs, many=True)
    return ser.data