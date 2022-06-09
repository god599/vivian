# coding=utf-8

"""
快递组件
"""
from api_call.http_util import *


class ExpressService(BaseHttp):
    def __init__(self, env):

        """
        初始化方法
        各个接口方法封装中需要的公共内容
        """
        BaseHttp.__init__(self, config_name="service.ini", env=env)
        self.set_host(self.host)
        self.set_token()

    # ====================== V1 ======================= #

    def get_search_express_info(self, search_url_data=None):
        """
        GET /query 查询资源标签
        返回值：ResourceTag 类型
        """
        url = '/query'
        method = 'GET'

        if search_url_data is not None:
            url_date = search_url_data.get()
            if len(url_date) != 0:
                url += '?' + urllib.urlencode(url_date, doseq=1)

        self.set_auth_exp(url=url, method=method)
        response = self.get(url)

        return response

    def post_search_word_info(self, search_url_data=None):
        """
        POST /suggest 查询单词
        返回值：
        """
        url = '/suggest'
        method = 'POST'
        if search_url_data is not None:
            url_data = search_url_data.get()
            if len(url_data) != 0:
                url += '?' + urllib.urlencode(url_data, doseq=1)

        self.set_auth_exp(url=url, method=method)
        response = self.post(url)

        return response
