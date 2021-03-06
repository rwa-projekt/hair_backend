from django.db import models
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from django.db.models.functions import Concat
from django.db.models import Value

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email = self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    
    name = models.CharField(max_length=80)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True, default=None, unique=True)
    role = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    class Meta:
        permissions = [
            ('view_client', 'Can View Client')
        ]


    def __str__(self):
        return self.name

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm: str):
        if self.is_superuser:
            return True
        permissions = set()
        perms = self.role.permissions.annotate(perm=Concat('content_type__app_label', Value('.'), 'codename')).values('perm')
        for p in perms:
            permissions.add(p['perm'])
        print(permissions)
        return perm in permissions

    def has_module_perms(self, app_label):
        return True

    def permissions(self):
        objs = Permission.objects.filter(group=self.role)
        arr = []
        for o in objs:
            arr.append(o.codename)
        return arr