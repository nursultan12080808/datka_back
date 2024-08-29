from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('news', NewsViewSet)
router.register('categories', CategoryViewSet)
router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('comments', CommentViewSet)
router.register('documents', DocumentViewSet)
router.register('chapters', ChapterViewSet)

urlpatterns = [
    # path('send_telegram/', TelegramSend),

    path('', include(router.urls)),
]