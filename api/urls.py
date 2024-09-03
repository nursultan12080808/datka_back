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
router.register('archives', ArchiveViewSet)

urlpatterns = [
    # path('send_telegram/', TelegramSend),
    path('auth/login/', LoginApiView.as_view()),
    path('auth/register/', RegisterApiView.as_view()),

    path('redactor_profile/<int:id>/', RedactorProfileApiView.as_view()),

    path('', include(router.urls)),
]