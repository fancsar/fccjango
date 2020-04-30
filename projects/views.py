import json
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from .models import Projects
from .models import ProjectsSerializer


def haha(request):
    return HttpResponse('<h1>Success</h1>')


# 使用类视图
class ProjectList(View):
    def get(self, request):
        projects = Projects.objects.all()
        project_list = ProjectsSerializer(instance=projects, many=True)
        return JsonResponse(data=project_list.data, safe=False)

    def post(self, request):
        json_data = request.body
        data = json.loads(json_data, encoding='utf-8')
        serializer = ProjectsSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(data=serializer.errors, status=400)
        project = Projects.objects.create(**serializer.validated_data)
        serializer = ProjectsSerializer(instance=project)
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
        serializer = ProjectsSerializer(instance=project)
        return JsonResponse(serializer.data, status=201)

    def post(self, request, pk):
        aa = [
            {'aa': 1, 'bb': 2},
            {'cc': 3, 'dd': 4}
        ]
        # return HttpResponse('<h1>Post  Success</h1>')
        return JsonResponse(aa, safe=False)

    def put(self, request):
        return HttpResponse('<h1>put Success</h1>')
