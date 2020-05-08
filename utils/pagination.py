


from rest_framework.pagination import PageNumberPagination


class ManualPageNumberPagination(PageNumberPagination):
    # 前端用户指定的页面key的名称
    page_query_param = 'p'
    # 前端用户指定的每一页条数key的名称
    page_size_query_param = 's'
    # 前端指定的每页最多数据条数
    max_page_size = 10

    page_size = 2