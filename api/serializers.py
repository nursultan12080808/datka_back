from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from drf_extra_fields.fields import Base64ImageField
from rest_framework.authtoken.models import Token
from shark_app.models import *




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'password', 'is_superuser', 'groups', 'user_permissions')



class NewsSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=Base64ImageField(), required=False)   
    class Meta:
        model = News
        exclude = ('user',)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"

class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'password', 'is_superuser', 'groups', 'user_permissions')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TagsSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Tags
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):

    new = NewsSerializer()
    commentator = DetailUserSerializer()

    class Meta:
        model = Comment
        fields = "__all__"


class DockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dock
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):

    dock_files = DockSerializer(many=True)

    class Meta:
        model = Document
        fields = "__all__"


class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = "__all__"


class DetailNewsSerializer(serializers.ModelSerializer):

    images = ImageSerializer(many = True)
    user = DetailUserSerializer()
    tags = TagsSerializer()
    category = CategorySerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = News
        fields = '__all__'


class ListNewsSerializer(serializers.ModelSerializer):

    images = ImageSerializer(many = True)
    user = DetailUserSerializer()
    tags = TagsSerializer()
    category = CategorySerializer()
    # comments = CommentSerializer()

    class Meta:
        model = News
        fields = "__all__"



    def update(self, instance, validated_data):
        images = validated_data.pop('images', [])
        new = super().update(instance, validated_data)
        for image in images:
            image_name = image.name
            image_file = image

            new_image = News.objects.create(new=new)
            new_image.image.save(image_name, image_file)
        return new
    

class CreateNewsSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=Base64ImageField(), required=False)   

    class Meta:
        model = News    
        fields = '__all__'

    @transaction.atomic()
    def create(self, validated_data):
        images = validated_data.pop('images', [])
        new = super().create(validated_data)

        for image in images:
            image_name = image.name
            image_file = image

            new_image = Images.objects.create(new = new)
            new_image.image.save(image_name, image_file)

        return new
    
class RegisterSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()  # Используем Base64ImageField вместо ListSerializer
    password1 = serializers.CharField(validators=[validate_password])
    password2 = serializers.CharField()

    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'password', 'is_superuser', 'groups', 'user_permissions',)

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        
        if password1 != password2:
            raise serializers.ValidationError({
                'password2': ['Пароли не совпадают!']
            })

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        validated_data['password'] = make_password(password)

        return super().create(validated_data)
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class DetailTokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Token
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'