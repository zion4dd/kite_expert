from rest_framework import serializers

from . import models


class KiteSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # brand = serializers.SlugRelatedField(read_only=True, slug_field='name')
    # expert = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = models.Kite
        fields = '__all__'
        # fields = ('id', 'name', 'text', 'time_create', 'time_update', 'is_published', 
        #           'brand', 'expert', 'photo1', 'photo2', 'photo3', 'photo4')


class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expert
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = '__all__'

