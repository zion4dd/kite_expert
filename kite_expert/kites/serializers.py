from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from kite_expert.settings import USER_IS_ACTIVE
from . import models


class KiteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # id = serializers.IntegerField(read_only=True)
    # brand = serializers.SlugRelatedField(read_only=True, slug_field='name')
    # user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = models.Kite
        # fields = '__all__'
        fields = ('id', 'name', 'text', 'time_create', 'time_update', 'is_published', 
                  'brand', 'photo1', 'photo2', 'photo3', 'photo4', 'user', 'user_id')


class ExpertSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Expert
        fields = '__all__'
        fields = ('id', 'user', 'about', 'photo', 'user_id')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = '__all__'


class MyUserCreateSerializer(UserCreateSerializer):
    is_active = serializers.HiddenField(default=USER_IS_ACTIVE)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'email', 'is_active')
