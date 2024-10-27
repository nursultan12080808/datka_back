from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from .filters import *
from .paginations import *
from .permissions import *
from .serializers import *
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


class ArchiveViewSet(ModelViewSet):
    queryset = Archive.objects.all()
    lookup_field = "id"
    serializer_class = ArchiveSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)


class PostanovlenieViewSet(ModelViewSet):
    queryset = Postanovlenie.objects.all()
    lookup_field = "id"
    serializer_class = PostanovlenieSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)


class AdministrationViewSet(ModelViewSet):
    queryset = Administration.objects.all()
    lookup_field = "id"
    serializer_class = AdministrationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)




class RegisterApiView(GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = DetailUserSerializer(user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key
        })
    
class LoginApiView(GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = DetailUserSerializer(user, context={'request': request})
            return Response({
                **user_serializer.data,
                'token': token.key
            })
        return Response({'detail': 'Не существуеет пользователя либо неверный пароль.'}, status.HTTP_400_BAD_REQUEST)


class RedactorProfileApiView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    lookup_field = 'id'
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            password = request.data.get('password')
            if(password):
                if check_password(password, user.password):
                    new_password = request.data.get('password1')
                    user.set_password(new_password)
                    user.save()
                else:
                    return Response({'error': 'Пароль неверный'}, status=status.HTTP_400_BAD_REQUEST)
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = DetailUserSerializer(user, context={'request': request})
            return Response({
                **user_serializer.data,
                'token': token.key
            })
    

class TokenViewSet(ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = {
        'list': DetailTokenSerializer,
        'retrieve': DetailTokenSerializer,
        'create': TokenSerializer,
        'update': TokenSerializer,
    }
    lookup_field = 'id'
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return self.serializer_class['update']
        return self.serializer_class[self.action] 