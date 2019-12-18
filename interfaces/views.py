from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from .models import Interfances

class InterfanceView(View):
    def get(self,request):


        Interfances.objects.create()
        return HttpResponse('新增数据成功')
