# coding=utf-8

"""
该模块封装属于当前服务的http基本操作
"""
import urllib
from nd.rest.co_http.http import Http
from nd.rest.co_token.uc import *
from nd.rest.conf.conf import MyCfg  # 引用配置方法

__author__ = "Administrator"


class BaseHttp(object):
    def __init__(self, config_name, env=None, language=None):
        """
        :param env: 指定配置文件中的环境名称
        """
        self.env = env
        self.language = language

        self.version = '1'      # 默认v1

        # 读配置文件，获取host等配置
        my_cfg = MyCfg(config_name)
        my_cfg.set_section(self.env)
        my_cfg.set_path(__file__)
        self.config = my_cfg

        try:
            self.port = my_cfg.get('port')
        except Exception as e:
            print "get port failed! reason: ", e
        self.host = my_cfg.get("host")
        self.gaea_id = my_cfg.get('gaea_id')
        self.user_id = my_cfg.get('user_id')
        self.project_id = my_cfg.get("project_id")
        self.user = my_cfg.get("user")
        self.password = my_cfg.get("password")

        self.header = dict()
        # self.header['Accept'] = 'application/json'
        self.header['Content-Type'] = 'application/json'
        # self.header['X-Gaea-Authorization'] = 'GAEA  id="{%s}"' %self.gaea_id
        # self.header['Authorization'] = 'USER user_id="%s",realm=""' %self.user_id

        # 声明默认的http对象（声明后才有具体实例）、header（设置后才生效）、版本号等
        self.http_o = None
        self.token_o = None

    def get_url(self, url):
        """
        url地址前面需要带上'/'
        :param url:不带版本号的url
        """
        #return "/v" + str(self.version) + url
        return url


    def set_host(self, host):
        """
        获取http实例
        """
        self.http_o = Http(host, self.port)
        self.http_o.set_header(self.header)

    def set_token(self):
        """
        根据环境，指定uc不同环境的token实例
        """
        if self.env == 'ol':
            uc_env = UcEnv.ol
        elif self.env == 'wjt':
            uc_env = UcEnv.wjt
        else:
            uc_env = UcEnv.pre
        self.token_o = UcToken(uc_env)

    def set_auth(self, token_type=2, user_name='', password='', org='', url='', method=''):
        """
        设置身份信息
        token_type:
            0: header中，不使用Authorization
            其他：header中带正确的Authorization
        """
        if user_name == '':
            user_name = self.user
        if password == '':
            password = self.password

        host = self.host
        # 加入端口会导致无法验证通过，去掉
        # if self.port != '' and self.port is not None:
        #     host += ':' + str(self.port)

        if self.language is not None:
            self.header['Accept-Language'] = self.language

        # 使用Gaea id进行项目隔离
        self.header['X-Gaea-Authorization'] = 'GAEA id="' + self.gaea_id + '"'
        my_access_token = self.token_o.get_token(user_name, password, org, self.get_url(url), method, host)
        print  my_access_token
        # 根据类型处理token
        if token_type == 0:
            self.remove_authorization()
        elif token_type == 1:  # 设置为错误的mac token
            self.header['Authorization'] = \
                'MAC id="930F04593E040BDAE507E54C00B84C4059008269612143E0835D2B9ED7C01C23",' \
                'nonce="1470724550000:9Sl9pGRo",mac="PRcoAuUzDZsrIxrcX+Pm+AYp+YI5ttR+KsRbdGJn8Ys="'
        # elif token_type == 6:
        #     mac_token = uc_token(self.env,self.config).get_mac_token(user_name,password,host,url,method)
        #     self.header['Authorization'] = mac_token
        else:
            # 可以使用固定账密，每次生成token
            access_token = self.token_o.get_token(user_name, password, org, self.get_url(url), method, host)
            self.header['Authorization'] = access_token

        self.http_o.set_header(self.header)

    def get(self, url):
        url = self.get_url(url)
        response = self.http_o.get(url)
        return response

    def post(self, url, body=None):
        url = self.get_url(url)
        if body is not None:
            body = json.dumps(body)
        response = self.http_o.post(url, body)
        return response

    def put(self, url, body=''):
        url = self.get_url(url)
        body = json.dumps(body)
        response = self.http_o.put(url, body)
        return response

    def delete(self, url, body=''):
        url = self.get_url(url)
        if body == '':
            response = self.http_o.delete(url)
        else:
            body = json.dumps(body)
            response = self.http_o.delete(url, body)
        return response

    def remove_authorization(self):
        if 'Authorization' in self.header.keys():
            self.header.pop('Authorization')
            self.http_o.set_header(self.header)

    def generate_url(self, url, params):
        # url中{ }通配符的对应变更
        while url.find('{') > -1:
            key_str = url[url.index('{') + 1: url.index('}')]
            url = url[0: url.index('{')] + params.pop(key_str) + url[url.index('}') + 1:]

        # 将url所有字符转换成url编码
        url = urllib.quote(url)

        # 处理Array类型的请求参数
        array_param = ''
        for key, value in params.items():
            if not isinstance(value, list):
                continue
            params.pop(key)
            for item in value:
                val = urllib.quote(key) + '=' + urllib.quote(str(item))
                array_param += '&' + val if len(array_param) > 0 else val

        # url拼接条件参数
        if len(params) > 0:
            if url.find('?') > 0:
                url += '&' + urllib.urlencode(params)
            else:
                url += '?' + urllib.urlencode(params)
        if len(array_param) > 0:
            if url.find('?') > 0:
                url += '&' + array_param
            else:
                url += '?' + array_param

        return url
        # return url + '?' + urllib.urlencode(params) if len(params) > 0 else url

#########################################################
    def set_auth_exp(self, url='', method=''):
        """
        设置身份信息
        token_type:
            0: header中，不使用Authorization
            其他：header中带正确的Authorization
        """
        host = self.host

        # 可以使用固定账密，每次生成token
        # access_token = self.token_o.get_token(self.get_url(url), method, host)
        # self.header['Authorization'] = access_token

        self.http_o.set_header(self.header)




