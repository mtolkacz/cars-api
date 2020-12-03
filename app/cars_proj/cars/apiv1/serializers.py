from rest_framework import serializers

from ..models import *


class PopularCarSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='car__id')
    model_name = serializers.CharField(source='car__model_name')
    make_name = serializers.CharField(source='car__make__make_name')
    count = serializers.IntegerField()

    def to_representation(self, instance):
        representation = super(PopularCarSerializer, self).to_representation(instance)
        representation['get_average_rate'] = Car.get_average_rate(instance['car__id'])
        return representation

    class Meta:
        model = Car
        fields = [
            'id',
            'model_name',
            'make_name',
            'get_average_rate',
            'count',
        ]


class CarSerializer(serializers.ModelSerializer):
    make_name = serializers.CharField(source='make.make_name')

    class Meta:
        model = Car
        fields = (
            'model_name',
            'make_name',
            'get_average_rate',
        )

