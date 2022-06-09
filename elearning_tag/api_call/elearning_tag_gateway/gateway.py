# coding=utf-8

"""
标签组件
"""
from api_call.http_util import *


class TagGateway(BaseHttp):
    def __init__(self, env):
        """
        初始化方法
        各个接口方法封装中需要的公共内容
        """
        BaseHttp.__init__(self, config_name="gateway.ini", env=env)
        self.set_host(self.host)
        self.set_token()

    def get_catalogs_tree(self, search_url_data=None, token_type=2):
        """
        GET /v1/tags/tree 获取标签树
        返回值:TagTreeVo 类型
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
