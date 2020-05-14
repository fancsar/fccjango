from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from .serializers import RegisterModleSerializer


class RegiserView(CreateAPIView):
    serializer_class = RegisterModleSerializer
    # 在类试图中全局指定权限(都可以访问)
    permission_classes = [permissions.AllowAny]
