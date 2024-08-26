from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from drf_extra_fields.fields import Base64ImageField
from rest_framework.authtoken.models import Token
from shark_app.models import *


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

    news = NewsSerializer()
    commentator = DetailUserSerializer()

    class Meta:
        model = Comment
        fields = "__all__"


class DetailNewsSerializer(serializers.ModelSerializer):

    images = ImageSerializer(many = True)
    user = DetailUserSerializer()
    tags = TagsSerializer()
    category = CategorySerializer()
    comments = CommentSerializer()

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
    
