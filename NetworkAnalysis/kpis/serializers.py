from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import CellUniqueUsersKPI, ServiceTrafficVolKPI


class CellUniqueUsersKPISerizliezer(serializers.ModelSerializer):

    class Meta:
        model = CellUniqueUsersKPI
        fields = '__all__'


class ServiceTrafficVolKPISerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceTrafficVolKPI
        fields = '__all__'


class KPIsSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='value')

    name = serializers.CharField()
