# -*- coding: utf-8 -*-
# @Time   :2020/5/14 19:12
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :get_SchemaGenerator.py
from rest_framework.schemas.coreapi import SchemaGenerator
from rest_framework.schemas.coreapi import LinkNode
from rest_framework.schemas.coreapi import insert_into
from rest_framework.schemas.coreapi import AutoSchema

class GETSchemaGenerator(SchemaGenerator):
    def get_links(self, request=None):
        """
        Return a dictionary containing all the links that should be
        included in the API schema.
        """
        links = LinkNode()

        paths, view_endpoints = self._get_paths_and_endpoints(request)

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        prefix = self.determine_path_prefix(paths)

        for path, method, view in view_endpoints:
            if method == 'GET':
                if not self.has_view_permissions(path, method, view):
                    continue
                link = view.schema.get_link(path, method, base_url=self.url)
                subpath = path[len(prefix):]
                keys = self.get_keys(subpath, method, view)
                insert_into(links, keys, link)

        return links

class MinAutoSchema(AutoSchema):
    pass
