# coding=utf-8

"""
标签组件
"""
from api_call.http_util import *


class TagService(BaseHttp):
    def __init__(self, env):
        """
        初始化方法
        各个接口方法封装中需要的公共内容
        """
        BaseHttp.__init__(self, config_name="service.ini", env=env)
        self.set_host(self.host)
        self.set_token()

    # ====================== V1 ======================= #
    def set_resources_tags(self, resource_tag_param, token_type=2):
        """
        PUT /v1/resources/tags 设置资源标签
        body参数：Array[ResourceTagParam] 类型
        返回值：无
        """
        self.version = 1
        url = '/resources/tags'
        method = 'PUT'
        body_data = [resource_tag_param.get()]

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.put(url, body_data)

        return response

    def get_search_resources_tags(self, search_url_data=None, token_type=2):
        """
        GET /v1/resources/tags/search 查询资源标签
        返回值：ResourceTag 类型
        """
        self.version = 1
        url = '/resources/tags/search'
        method = 'GET'

        if search_url_data is not None:
            url_data = search_url_data.get()
            if len(url_data) != 0:
                url += '?' + urllib.urlencode(url_data, doseq=1)

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.get(url)

        return response

    def post_search_resources_tags(self, search_url_data, token_type=2):
        """
        POST /v1/resources/tags/search 查询资源标签
        返回值：ResourceTag 类型
        """
        self.version = 1
        url = '/resources/tags/search'

        method = 'POST'

        if search_url_data is not None:
            url_data = search_url_data.get()
            if len(url_data) != 0:
                url += '?' + urllib.urlencode(url_data, doseq=1)

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.post(url)

        return response

    def search_tags(self, tag_ids, token_type=2):
        """
        GET /v1/tags 查询标签
        返回值：Array[TagVo] 类型
        """
        self.version = 1
        url = '/tags'
        method = 'GET'

        if tag_ids is not None:
            if len(tag_ids) != 0:
                url = '/tags' + '?tag_ids=' + str(tag_ids)

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.get(url)

        return response

    def add_tags(self, tagvo, token_type=2):
        """
        POST /v1/tags 创建标签
        body参数：TagVo 类型
        返回值：TagVo 类型
        """
        self.version = 1
        url = '/tags'
        method = 'POST'
        body_data = tagvo.get()

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.post(url, body_data)

        return response

    def search_tags_tree(self, search_url_data, token_type=2):
        """
        GET /v1/tags/tree 查询标签树
        返回值：TagTreeVo 类型
        """
        self.version = 1
        url = '/tags/tree'
        method = 'GET'
        if search_url_data is not None:
            url_data = search_url_data.get()
            if len(url_data) != 0:
                url += '?' + urllib.urlencode(url_data, doseq=1)
        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.get(url)

        return response

    def according_to_tag_id_to_search_tags_tree_children(self, tag_id, token_type=2):
        """
        GET /v1/tags/tree/children 根据标签标识查询子标签树
        返回值：TagTreeVo 类型
        """
        self.version = 1
        url = '/tags/tree/children'
        method = 'GET'

        if tag_id is not None:
            if len(tag_id) != 0:
                url = '/tags/tree/children' + '?tag_id=' + str(tag_id)

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.get(url)

        return response

    def search_tags_tree_without_sort(self, search_url_data, token_type=2):
        """
        GET /v1/tags/treewithoutsort 查询标签树(无排序)
        返回值：Array[Tag] 类型
        """
        self.version = 1
        url = '/tags/treewithoutsort'
        method = 'GET'
        if search_url_data is not None:
            url_data = search_url_data.get()
            if len(url_data) != 0:
                url += '?' + urllib.urlencode(url_data, doseq=1)

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.get(url)

        return response

    def search_tags_id(self, tag_id, token_type=2):
        """
        GET /v1/tags/{tag_id} 查询标签
        返回值：TagVo 类型
        """
        self.version = 1
        url = '/tags/' + str(tag_id)
        method = 'GET'

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.get(url)

        return response

    def compile_tags(self, tag_id, tags_object, token_type=2):
        """
        PUT /v1/tags/{tag_id} 修改标签
        返回值：TagVo 类型
        """
        self.version = 1
        url = '/tags/' + str(tag_id)
        method = 'GET'
        body_data = tags_object.get()

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.put(url, body_data)

        return response

    def delete_tags(self, tag_id, token_type=2):
        """
        DELETE /v1/tags/{tag_id} 删除标签(与资源关系也删除)
        返回值：
        """
        self.version = 1
        url = '/tags/' + str(tag_id)
        method = 'DELETE'

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.delete(url)

        return response

    def move_tags(self, tag_id, tag_move_param, token_type=2):
        """
        PUT /v1/tags/{tag_id}/move 移动标签
        返回值：
        """
        self.version = 1
        url = '/tags/' + str(tag_id) + '/move'
        method = 'PUT'
        body_data = tag_move_param.get()

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.put(url, body_data)

        return response

    # ====================== V2 ======================= #

    def search_tags_v2(self, tag_ids, token_type=2):
        """
        GET /v2/tags 查询标签
        返回值：Array[TagVo] 类型
        """
        self.version = 2
        url = '/tags'
        method = 'GET'

        if tag_ids is not None:
            if len(tag_ids) != 0:
                url = '/tags' + '?tag_ids=' + str(tag_ids)

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.get(url)

        return response

    def add_tags_v2(self, tagvo, token_type=2):
        """
        POST /v2/tags 创建标签
        body参数：TagVo 类型
        返回值：TagVo 类型
        """
        self.version = 2
        url = '/tags'
        method = 'POST'
        body_data = tagvo.get()

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.post(url, body_data)

        return response

    def search_tags_list_v2(self, body_data, token_type=2):
        """
        POST /v2/tags/list 查询标签
        返回值：TagVo 类型
        """
        self.version = 2
        url = '/tags/list'
        method = 'POST'
        body_data = body_data.get()

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.put(url, body_data)

        return response

    def search_tags_tree_v2(self, search_url_data, token_type=2):
        """
        GET /v2/tags/tree 查询标签树
        返回值：TagTreeVo 类型
        """
        self.version = 2
        url = '/tags/tree'
        method = 'GET'
        if search_url_data is not None:
            url_data = search_url_data.get()
            if len(url_data) != 0:
                url += '?' + urllib.urlencode(url_data, doseq=1)
        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.get(url)

        return response

    def according_to_tag_id_to_search_tags_tree_children_v2(self, tag_id, token_type=2):
        """
        GET /v2/tags/tree/children 根据标签标识查询子标签树
        返回值：TagTreeVo 类型
        """
        self.version = 2
        url = '/tags/tree/children'
        method = 'GET'

        if tag_id is not None:
            if len(tag_id) != 0:
                url = '/tags/tree/children' + '?tag_id=' + str(tag_id)

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.get(url)

        return response

    def search_tags_tree_without_sort_v2(self, search_url_data, token_type=2):
        """
        GET /v2/tags/treewithoutsort 查询标签树(无排序)
        返回值：Array[Tag] 类型
        """
        self.version = 2
        url = '/tags/treewithoutsort'
        method = 'GET'
        if search_url_data is not None:
            url_data = search_url_data.get()
            if len(url_data) != 0:
                url += '?' + urllib.urlencode(url_data, doseq=1)

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.get(url)

        return response

    def search_tags_id_v2(self, tag_id, token_type=2):
        """
        GET /v2/tags/{tag_id} 查询标签
        返回值：TagVo 类型
        """
        self.version = 2
        url = '/tags/' + str(tag_id)
        method = 'GET'

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.get(url)

        return response

    def compile_tags_v2(self, tag_id, tags_object, token_type=2):
        """
        PUT /v2/tags/{tag_id} 修改标签
        返回值：TagVo 类型
        """
        self.version = 2
        url = '/tags/' + str(tag_id)
        method = 'GET'
        body_data = tags_object.get()

        self.set_auth(token_type=token_type, url=url, method=method)
        response = self.put(url, body_data)

        return response
