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