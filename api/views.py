from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from .filters import *
from .paginations import *
from .permissions import *
from .serializers import *
import telegram_send
from shark_app.models import *
from django.contrib.auth.views import get_user_model

User = get_user_model()

# @api_view(["POST"])
# async def TelegramSend(request):
#     text = request.data.get("text")
#     if not text:
#         return Response({"error": "Text is required"}, status=400)
#     try:
#         await telegram_send.send(messages=[text])
#         return Response({"status": "Message sent successfully"}, status=200)
#     except Exception as e:
#         return Response({"error": str(e)}, status=500)

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


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    lookup_field = "id"
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)


class ChapterViewSet(ModelViewSet):
    queryset = Chapter.objects.all()
    lookup_field = "id"
    serializer_class = ChapterSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)

