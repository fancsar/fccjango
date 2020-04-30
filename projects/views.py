from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from .models import Projects


def haha(request):
    return HttpResponse('<h1>Success</h1>')


# 使用类视图

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
        if isinstance(project, JsonResponse):
            return project
        new_dict = {
            'id': project.id,
            'name': project.name,
            'leader': project.leader,
            'tester': project.tester,
            'programer': project.programmer,
            'publish_app': project.publish_app,
            'desc': project.desc
        }
        return JsonResponse(new_dict)

    def post(self, request, pk):
        aa = [
            {'aa': 1, 'bb': 2},
            {'cc': 3, 'dd': 4}
        ]
        # return HttpResponse('<h1>Post  Success</h1>')
        return JsonResponse(aa, safe=False)

    def put(self, request):
        return HttpResponse('<h1>put Success</h1>')
