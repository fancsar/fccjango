from rest_framework import serializers

from .models import Interfaces
from projects.models import Projects


class InterfacesModelSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目', help_text='所属项目', queryset=Projects.objects.all())

    class Meta:
        model = Interfaces
        # fields = '__all__'
        fields = ('id', 'name', 'tester', 'desc', 'project_id')

