from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from .filters import *
from .paginations import *
from .permissions import *
from .serializers import *
from shark_app.models import *

from django.contrib.auth.views import get_user_model

User = get_user_model()

class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    lookup_field = "id"
    serializer_class = {
        'list': ListNewsSerializer,
        'retrieve': DetailNewsSerializer,
        'create': CreateNewsSerializer,
        'update': NewsSerializer,
    }
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NewsFilter
    pagination_class = MediumPagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return self.serializer_class['update']
        return self.serializer_class[self.action] 
    

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    lookup_field = "id"
    serializer_class = CategorySerializer



class TagViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    lookup_field = "id"
    serializer_class = TagsSerializer



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    lookup_field = "id"
    serializer_class = DetailUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    lookup_field = "id"
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)
