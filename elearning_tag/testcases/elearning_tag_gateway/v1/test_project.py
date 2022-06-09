# coding=utf-8

from api_call.elearning_tag_gateway.gateway import TagGateway
from data_struct.gateway.gateway_data import *
from config.gbl import *


class TagTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rest_o = Restful()
        cls.rand_o = CoRand()
        cls.tag_o = TagGateway(env=ENVIRONMENT)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # -------------------- /v1/tags/tree ------------------------ #
    # -------------------- GET 获取标签树------------------------ #
    def test_get_tags_tree_no_pass_parameter(self):
        """
        custom_type和need_photo_url为选填项，不传这两个参数，获取标签树
        【done】
        level:1,2,3,4,5,6,7
        """
        search_url = TagTreeParameter()
        res = self.tag_o.get_catalogs_tree(search_url)
        self.rest_o.parse_response(res, OK, "获取标签树失败")

    def test_get_tags_tree_pass_custom_type_ok(self):
        """
        传入存在的custom_type，如：custom_type='el-learning-unit'（资源池标签），不传入need_photo_url，获取标签树
        【done】
        level:1,2,3,4,5,6
        """
        search_url = TagTreeParameter(custom_type='el-learning-unit')
        res = self.tag_o.get_catalogs_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "获取标签树失败")
        # 验证数据
        if data_dict:
            TagTreeData(data_dict)
            assert_that(data_dict['custom_type'], equal_to('el-learning-unit'))

    def test_get_tags_tree_pass_nonexistent_custom_type(self):
        """
        传入不存在的custom_type，如：custom_type='el-learning-unit1'（资源池标签），不传入need_photo_url，获取标签树
        【done】
        level:1,2,3,4,5,6
        """
        search_url = TagTreeParameter(custom_type='el-learning-unit1')
        res = self.tag_o.get_catalogs_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "获取标签树失败")
        # 验证数据：成功，无返回信息
        assert_that(data_dict, equal_to({}))

    def test_get_tags_tree_pass_need_photo_url_equal_to_true(self):
        """
        传入need_photo_url参数，need_photo_url为true，获取标签树
        【done】
        level:1,2,3,4,5,6
        """
        search_url = TagTreeParameter(custom_type='el-learning-unit', need_photo_url='true')
        res = self.tag_o.get_catalogs_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "获取标签树失败")
        if data_dict:
            TagTreeData(data_dict)

    def test_get_tags_tree_pass_need_photo_url_equal_to_false(self):
        """
        传入need_photo_url参数，need_photo_url为false，不传入custom_type，获取标签树
        【done】
        level:1,2,3,4,5,6
        """
        search_url = TagTreeParameter(custom_type='el-learning-unit', need_photo_url='false')
        res = self.tag_o.get_catalogs_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "获取标签树失败")
        if data_dict:
            TagTreeData(data_dict)

    def test_get_tags_tree_pass_need_photo_url(self):
        """
        传入need_photo_url参数，need_photo_url为错误值true1，不传入custom_type，获取标签树
        【done】
        level:1,2,3,4,5,6
        """
        search_url = TagTreeParameter(custom_type='el-learning-unit', need_photo_url='true1')
        res = self.tag_o.get_catalogs_tree(search_url)
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "获取标签树成功")
