from rest_framework import serializers
from .models import Interfaces


class InterfacesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        # fields = '__all__'
        fields = ('id', 'name', 'tester', 'desc', 'project_id')
