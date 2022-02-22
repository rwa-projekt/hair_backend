from rest_framework import serializers, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Account
from .serializers import *
from .selector import *
from .permissions import *


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        request.data['username'] = request.data['email']
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        account = BasicUserSerializer(user).data

        data = {
            'token': token.key,
            'account': account
            }

        return Response(data, 200)


class GetUserApiView(APIView):

    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        if 'token' in request.GET:
            token = request.GET['token']
            res = get_user(token)
            return Response(res, 200)
        else:
            return Response({"message": "Token"}, status.HTTP_401_UNAUTHORIZED)


class AccountViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin):
    """
    Registracija korisnika...
    """
    queryset = Account.objects.filter(is_active=True).order_by('name')
    serializer_class = BasicUserSerializer
    permission_classes = (AccountPermission, )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        if not 'password' in request.data:
            return Response({"message": "Password missing"}, 404)
        ser = InsertUserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        token, created = Token.objects.get_or_create(user_id=ser.data['id'])
        user = token.user
        user.set_password(request.data['password'])
        user.save()
        account = BasicUserSerializer(user).data

        data = {
            'token': token.key,
            'account': account
            }

        return Response(data, 200)

    @action(detail=False, methods=['GET'])
    def barbers(self, request, *args, **kwargs):
        res = get_barbers()
        return Response(res, 200)