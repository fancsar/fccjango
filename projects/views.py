import json
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from .models import Projects
from .serializers import ProjectsModelSerializer


def haha(request):
    return HttpResponse('<h1>Success</h1>')


# 使用类视图
class ProjectList(View):
    def get(self, request):
        projects = Projects.objects.all()
        project_list = ProjectsModelSerializer(instance=projects, many=True)
        return JsonResponse(data=project_list.data, safe=False)

    def post(self, request):
        json_data = request.body
        data = json.loads(json_data, encoding='utf-8')
        serializer = ProjectsModelSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return JsonResponse(data=serializer.errors, status=400)
        serializer.save()
        return JsonResponse(serializer.data, status=201)


class IndexView(View):
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
        return JsonResponse(serializer.data, status=201)

    def post(self, request, pk):
        json_data = request.body
        data = json.loads(json_data, encoding='utf-8')
        project = self.get_object(pk)
        serializer = ProjectsModelSerializer(data=data, instance=project)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return JsonResponse(serializer.errors, status=400)
        serializer.save()
        return JsonResponse(serializer.data, status=201)

    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return JsonResponse(None, safe=True, status=204)

