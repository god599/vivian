# coding=utf-8

from api_call.express.service import ExpressService
from data_struct.service.service_data import *
from config.gbl import *


class ExpressTest(unittest.TestCase):

    # 必须使用@classmethod 装饰器,  所有case运行之前只运行一次
    @classmethod
    def setUpClass(cls):
        # 断言库对象
        cls.rest_o = Restful()
        # 生成随机串
        cls.rand_o = CoRand()
        # 配置（host、token）、环境
        cls.tag_o = ExpressService(env=ENVIRONMENT)
    '''
    # 每个测试case运行之前运行
    def setUp(self):
        # 资源列表，用以回收资源
        self.tag_id_list = list()
    '''

    # --------------------- /v1/resources/tags/search ------------------------ #
    # -------------------------- GET 查询资源标签 ----------------------------- #
    '''
    def test_get_search_express_with_parameter(self):
        """
        选填：$type、$postid，参数正常传，查询结果
        【done】
        level:1,2,3,4,5,6,7
        """
        # 正常传参数
        type = 'yunda'
        postid = '462073548135931'
        search_url = ExpressParamData(type=type, postid=postid)
        # 拼接地址，发起请求
        res = self.tag_o.get_search_express_info(search_url)
        # 断言
        self.rest_o.parse_response(res, OK, "ok")

    def test_get_search_express_no_parameter(self):
        """
        选填：$type、$postid，参数不传，查询结果
        【done】
        level:1,2,3,4,5,6,7
        """
        # 不传参数

        search_url = ExpressParamData()
        # 拼接地址，发起请求
        res = self.tag_o.get_search_express_info(search_url)
        # 断言
        self.rest_o.parse_response(res, OK, "参数错误")

    def test_get_search_express_wrong_parameter(self):
        """
        选填：$type、$postid，参数不传，查询结果
        【done】
        level:1,2,3,4,5,6,7
        """
        #
        type = 'abc'
        postid = '123'
        search_url = ExpressParamData(type=type, postid=postid)
        # 拼接地址，发起请求
        res = self.tag_o.get_search_express_info(search_url)
        # 断言
        self.rest_o.parse_response(res, OK, "参数错误")
    '''

    def test_post_word_with_body(self):
        """
        body
        q = money
        num = 1
        doctype = json
        【done】
        level:1,2,3,4,5,6
        """
        # 使用
        q = 'money'
        num = '1'
        doctype = 'json'
        search_body = WordParamData(q=q, num=num, doctype=doctype)
        # 拼接地址，发起请求
        res = self.tag_o.post_search_word_info(search_body)
        # 断言
        self.rest_o.parse_response(res, OK, "success")

        #ResourceTag(data_dict1['items'][0])
        #assert_that(data_dict1['items'][0]['id'], equal_to(tag_id))


    '''
        if data_dict:
            for i in data_dict['items']:
                ResourceTag(i)
    def test_get_resources_tags_use_filter(self):
        """
        $filter（其他参数不传）
        $filter = 正确的取值，如：$filter = tag_id eq xxx（标签标识），查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        # 使用查询标签树，查询存在的id（标签标识）
        search_url = ExpressParamData()
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")
        tag_id = data_dict['items'][0]['id']

        filter = 'id eq ' + str(tag_id)
        search_url = ExpressParamData(filter=filter)
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        ResourceTag(data_dict1['items'][0])
        assert_that(data_dict1['items'][0]['id'], equal_to(tag_id))

    def test_get_resources_tags_use_none_filter(self):
        """
        $filter（其他参数不传）
        传入空$filter串，查询资源标签
        【done】
        level:1,3,5
        """
        search_url = SearchResourceTagData(filter='')
        res = self.tag_o.get_search_resources_tags(search_url)
        self.rest_o.parse_response(res, OK, "查询资源标签失败")

    '''
