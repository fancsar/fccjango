import json
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Projects
from .serializers import ProjectsModelSerializer


def haha(request):
    return HttpResponse('<h1>Success</h1>')


# 使用类视图
class ProjectList(APIView):
    def get(self, request):
        projects = Projects.objects.all()
        project_list = ProjectsModelSerializer(instance=projects, many=True)
        return Response(data=project_list.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectsModelSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IndexView(APIView):
    '''
    index: 主页类视图
    1.类视图需要继承View或者View子类
    2.实例方法get,post,put,delete（全部小写），与其响应的请求方法一一对应
    3.方法的第一个参数为，该视图对象本身，第二个为HttpRequest请求对象
    4. 
    '''

    def get_object(self, pk):
        try:
            return Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectsModelSerializer(instance=project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectsModelSerializer(data=request.data, instance=project)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
