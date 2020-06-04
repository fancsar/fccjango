from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .models import DebugTalks
from .serializers import DebugTalksModelSerializer


class DebugTalksList(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = DebugTalks.objects.all()
    serializer_class = DebugTalksModelSerializer

    def retrieve(self, request, *args, **kwargs):
        debugtalk_obj = self.get_object()
        data = {
            'id': debugtalk_obj.id,
            'debugtalks': debugtalk_obj.debugtalk
        }
        return Response(data)
