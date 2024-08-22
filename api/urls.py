from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('news', NewsViewSet)
router.register('categories', CategoryViewSet)
router.register('users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
]