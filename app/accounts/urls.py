from django.urls import path, include
from rest_framework import routers, viewsets
from . import views

router = routers.DefaultRouter()
router.register('accounts', views.AccountViewSet)
# router.register('register', views.RegisterViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('register/', views.AccountCreate.as_view()),
    path('auth/', views.CustomAuthToken.as_view()),
    path('getuser/', views.GetUserApiView.as_view(), name='getUserByToken')
]
