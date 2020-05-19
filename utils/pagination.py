from rest_framework.pagination import PageNumberPagination


class ManualPageNumberPagination(PageNumberPagination):
    # 前端用户指定的页面key的名称
    page_query_param = 'page'
    page_query_description = '第几页'
    # 前端用户指定的每一页条数key的名称
    page_size_query_param = 'size'
    page_size_query_description = '每页几条'
    # 前端指定的每页最多数据条数
    max_page_size = 10

    page_size = 2

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        response.data['current_page_num'] = self.page.number
        return response
