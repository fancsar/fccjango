import json

from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render

# Create your views here.
from django.views import View
from .models import Interfaces
from .serializers import InterfacesModelSerializer


class InterfanceList(View):
    def get(self, request):
        interfaces = Interfaces.objects.all()
        serializer = InterfacesModelSerializer(instance=interfaces, many=True)
        return JsonResponse(serializer.data, safe=False, status=201)

    def post(self, request):
        json_data = request.body
        data = json.loads(json_data)
        serializer = InterfacesModelSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            JsonResponse(Http404, status=400)
        serializer.save()
        return JsonResponse(serializer.data, status=201)


class InterfacesDetail(View):
    def get_object(self, pk):
        try:
            return Interfaces.objects.get(pk=pk)
        except Interfaces.DoesNotExist:
            return Http404

    def get(self, request, pk):
        interface = self.get_object(pk)
        serializer = InterfacesModelSerializer(instance=interface)
        return JsonResponse(serializer.data, status=201)

    def post(self, request, pk):
        json_data = request.body
        data = json.loads(json_data, encoding='utf-8')
        interface = self.get_object(pk)
        serializer = InterfacesModelSerializer(data=data, instance=interface)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            JsonResponse(Http404, status=400)
        serializer.save()
        return JsonResponse(serializer.data, status=201)

    def delete(self, request, pk):
        interface = self.get_object(pk)
        interface.delete()
        return JsonResponse(None, status=204, safe=False)
