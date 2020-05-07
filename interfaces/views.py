import json

from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Interfaces
from .serializers import InterfacesModelSerializer


class InterfanceList(APIView):
    def get(self, request):
        interfaces = Interfaces.objects.all()
        serializer = InterfacesModelSerializer(instance=interfaces, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request):
        serializer = InterfacesModelSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            Response(Http404, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InterfacesDetail(APIView):
    def get_object(self, pk):
        try:
            return Interfaces.objects.get(pk=pk)
        except Interfaces.DoesNotExist:
            return Http404

    def get(self, request, pk):
        interface = self.get_object(pk)
        serializer = InterfacesModelSerializer(instance=interface)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, pk):
        interface = self.get_object(pk)
        serializer = InterfacesModelSerializer(data=request.data, instance=interface)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            Response(Http404, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        interface = self.get_object(pk)
        interface.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
