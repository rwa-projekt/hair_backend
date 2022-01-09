from django.urls import path, include
from rest_framework import routers, viewsets
from . import views

router = routers.DefaultRouter()
router.register('hair_styles', views.HairStyleViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('register/', views.AccountCreate.as_view()),
]
