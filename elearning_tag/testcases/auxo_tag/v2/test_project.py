# coding=utf-8

from api_call.auxo_tag.service import TagService
from data_struct.service.service_data import *
from config.gbl import *


class TagTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rest_o = Restful()
        cls.rand_o = CoRand()
        cls.tag_o = TagService(env=ENVIRONMENT)

    def setUp(self):
        # 资源列表，用以回收资源
        self.tag_id_list = list()

    def tearDown(self):
        # 回收资源
        if len(self.tag_id_list) != 0:
            for tag_id in self.tag_id_list:
                self.tag_o.delete_tags(tag_id)

    # ------------------------ /v2/tags ------------------------ #
    # ---------------------- GET 查询标签 ------------------------ #
    # 传入存在的标签标识，查询标签 --------在创建标签中覆盖
    def test_search_tags_use_wrong_params_v2(self):
        """
        传入不存在的标签标识，查询标签
        【done】
        level:1,3,5
        """
        # 传入不存在的标签标识（格式正确），查询标签
        res = self.tag_o.search_tags_v2(tag_ids='1f01f0df-af7f-4396-8355-e1234b912342')
        # 成功，返回数据为空
        data_dict = self.rest_o.parse_response(res, OK, "查询标签失败")
        assert_that(data_dict, equal_to([]))

        # 传入不存在的标签标识（格式错误），查询标签
        res = self.tag_o.search_tags_v2(tag_ids='1232455454')
        # 失败
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询标签失败")

    def test_search_tags_no_use_params_v2(self):
        """
        不传入标签标识，查询标签
        【done】
        level:1,3,5
        """
        res = self.tag_o.search_tags_v2(tag_ids=None)
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询标签失败")

    # ------------------------ /v2/tags ------------------------- #
    # ---------------------- POST 创建标签 ----------------------- #
    def test_add_tags_pass_title_v2(self):
        """
        传入title，创建标签
        【done】
        level:1,2,3,4,5,6,7
        """
        # 传入title，创建标签
        title = 'api_标签名称' + self.rand_o.randomword(5)
        search_url = TagData(title=title)
        res = self.tag_o.add_tags_v2(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "创建标签失败")
        TagVo(data_dict)
        tag_id = data_dict['id']
        self.tag_id_list.append(tag_id)

        # 查询标签
        res = self.tag_o.search_tags_v2(tag_id)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询标签失败")
        TagVo(data_dict)
        assert_that(data_dict1[0]['title'], equal_to(title))

        # 删除标签
        res = self.tag_o.delete_tags(tag_id=tag_id)
        self.rest_o.parse_response(res, OK, "删除标签失败")
        self.tag_id_list = []
        TagVo(data_dict)

    def test_add_tags_no_pass_title_v2(self):
        """
        不传入title，创建标签
        【done】
        level:1,3,5
        """
        # 不传入title，创建标签
        search_url = TagData()
        res = self.tag_o.add_tags_v2(search_url)
        # 500，提建议
        self.rest_o.parse_response(res, 500, "创建标签失败")

    # -------------------- /v2/tags/list ------------------------ #
    # -------------------- POST 查询标签 ------------------------ #

    # -------------------- /v2/tags/tree ------------------------ #
    # -------------------- GET 查询标签树 ------------------------ #
    def test_get_tags_tree_v2(self):
        """
        传入存在的自定义类型，如el-learning-unit（资源池标签），获取标签树
        【done】
        level:1,2,3,4,5,6,7
        """
        custom_type = 'el-learning-unit'
        search_url = TagTreeParameter(custom_type=custom_type)
        res = self.tag_o.search_tags_tree_v2(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "获取标签失败")
        if data_dict:
            TagTreeVo(data_dict)

    def test_get_tags_tree_pass_wrong_custom_type_v2(self):
        """
        传入不存在的自定义类型，如el-learning-unit1（资源池标签），获取标签树
        【done】
        level:1,3,5
        """
        custom_type = 'el-learning-unit1'
        search_url = TagTreeParameter(custom_type=custom_type)
        res = self.tag_o.search_tags_tree_v2(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "获取标签失败")
        assert_that(data_dict, equal_to({}))

    def test_get_tags_tree_no_pass_custom_type_v2(self):
        """
        不传入自定义类型，获取标签树
        【done】
        level:1,3,5
        """
        search_url = TagTreeParameter()
        res = self.tag_o.search_tags_tree_v2(search_url)
        data_dict = self.rest_o.parse_response(res, REQUIRE_ARGUMENT, "获取标签失败")

    # ----------------------- /v2/tags/tree/children ------------------------- #
    # -------------------- GET 根据标签标识查询子标签树 ------------------------ #
    def test_search_tags_tree_children_use_params_v2(self):
        """
        传入存在的标签标识，查询子标签树
        【done】
        level:1,3,4,5,6,7
        """
        # 查询标签树，获取标签标识
        search_url = TagTreeParameter()
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询子标签树失败")
        tag_id = data_dict['children'][0]['id']

        # 传入存在的标签标识，查询子标签树
        res = self.tag_o.according_to_tag_id_to_search_tags_tree_children_v2(tag_id)
        data_dict = self.rest_o.parse_response(res, OK, "查询子标签树失败")
        TagTreeVo(data_dict)

    def test_search_tags_tree_children_use_wrong_params_v2(self):
        """
        传入不存在的标签标识，查询子标签树
        【done】
        level:1,3,5
        """
        # 传入不存在的标签标识（格式正确），查询标签
        res = self.tag_o.according_to_tag_id_to_search_tags_tree_children_v2(tag_id='1f01f0df-af7f-4396-8355-e1234b912342')

        # 失败（目前报500，已提建议）
        self.rest_o.parse_response(res, 500, "查询子标签树失败")

        # 传入不存在的标签标识（格式错误），查询标签
        res = self.tag_o.according_to_tag_id_to_search_tags_tree_children_v2(tag_id='1232455454')
        # 失败
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询子标签树失败")

    def test_search_tree_children_tags_no_use_params_v2(self):
        """
        不传入标签标识，查询标签
        【done】
        level:1,3,5
        """
        res = self.tag_o.according_to_tag_id_to_search_tags_tree_children_v2(tag_id=None)
        self.rest_o.parse_response(res, REQUIRE_ARGUMENT, "查询子标签树失败")

    # ------------------------ /v2/tags/treewithoutsort ------------------------- #
    # -------------------------- GET 查询标签树(无排序) -------------------------- #
    def test_get_tags_tree_without_sort_no_pass_parameter_v2(self):
        """
        custom_id和custom_type为选填项，不传这两个参数,查询标签树（无排序）
        【done】
        level:1,2,3,4,5,6,7
        """
        search_url = TagTreeCustomParameter()
        res = self.tag_o.search_tags_tree_without_sort_v2(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询标签树失败")
        for i in data_dict:
            Tag(i)

    def test_get_tags_tree_without_sort_pass_custom_id_v2(self):
        """
        传入存在的custom_id，不传入custom_type，查询标签树
        【done】
        level:1,3,4,5
        """
        # 查询标签树，获取custom_id
        search_url = TagTreeParameter()
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询标签树失败")
        custom_id = data_dict['children'][0]['custom_id']

        search_url = TagTreeCustomParameter(custom_id=custom_id)
        res = self.tag_o.search_tags_tree_without_sort_v2(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询标签树失败")
        Tag(data_dict1[0])
        assert_that(data_dict1[0]['custom_id'], equal_to(custom_id))

    def test_get_tags_tree_without_sort_pass_nonexistent_custom_id_v2(self):
        """
        传入不存在的custom_id，，不传入need_photo_url，查询标签树
        【done】
        level:1,3,5
        """
        search_url = TagTreeCustomParameter(custom_id='custom_id1')
        res = self.tag_o.search_tags_tree_without_sort_v2(search_url)
        self.rest_o.parse_response(res, OK, "查询标签树失败")

        # 查询标签时，若没有标签，该项目存在根节点标签时，返回根节点标签。

    def test_get_tags_tree_without_sort_pass_custom_type_v2(self):
        """
        传入存在的custom_type，不传入custom_id，查询标签树
        【done】
        level:1,3,4,5
        """
        # 查询标签树，获取custom_type
        search_url = TagTreeParameter()
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询标签树失败")
        custom_type = data_dict['children'][0]['custom_type']

        search_url = TagTreeCustomParameter(custom_type=custom_type)
        res = self.tag_o.search_tags_tree_without_sort_v2(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询标签树失败")
        Tag(data_dict1[0])
        assert_that(data_dict1[0]['custom_type'], equal_to(custom_type))

    def test_get_tags_tree_without_sort_pass_nonexistent_custom_type_v2(self):
        """
        传入不存在的custom_type，不传入custom_id，查询标签树
        【done】
        level:1,3,5
        """
        search_url = TagTreeCustomParameter(custom_type='el-channel1')
        res = self.tag_o.search_tags_tree_without_sort_v2(search_url)
        self.rest_o.parse_response(res, OK, "查询标签树失败")

    def test_get_tags_tree_without_sort_pass_two_parameter_v2(self):
        """
        custom_type和custom_id为选填项，传这两个参数，搜索标签树
        【done】
        level:1,3,4,5
        """
        # 查询标签树，获取custom_type和custom_id
        search_url = TagTreeParameter()
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询标签树失败")
        custom_id = data_dict['children'][0]['custom_id']
        custom_type = data_dict['children'][0]['custom_type']

        search_url = TagTreeCustomParameter(custom_id=custom_id, custom_type=custom_type)
        res = self.tag_o.search_tags_tree_without_sort_v2(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询标签树失败")
        Tag(data_dict1[0])
        assert_that(data_dict1[0]['custom_id'], equal_to(custom_id))
        assert_that(data_dict1[0]['custom_type'], equal_to(custom_type))

    # ------------------------ /v2/tags/{tag_id} ------------------------ #
    # -------------------------- GET 查询标签 ---------------------------- #
    def test_search_tags_use_url_v2(self):
        """
        传入存在的标签标识，查询标签
        【done】
        level:1,2,3,4,5,6,7
        """
        # 查询标签树，获取标签标识
        search_url = TagTreeParameter()
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询标签失败")
        tag_id = data_dict['children'][0]['id']

        # 传入存在的标签标识，查询标签
        res = self.tag_o.search_tags_id_v2(tag_id)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询标签失败")

        assert_that(data_dict1['id'], equal_to(tag_id))

    def test_search_tags_use_wrong_url_v2(self):
        """
        传入不存在的标签标识，查询标签
        【done】
        level:1,3,5
        """
        # 传入不存在的标签标识（格式正确），查询标签
        res = self.tag_o.search_tags_id_v2(tag_id='5f543ae7-b489-4ada-a1ae-dd34dbe3a123')
        # 成功，返回数据为空
        data_dict = self.rest_o.parse_response(res, OK, "查询标签失败")
        assert_that(data_dict, equal_to({}))

        # 传入不存在的标签标识（格式错误），查询标签
        res = self.tag_o.search_tags_id_v2(tag_id='1232455454')
        # 失败
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询标签失败")

    # ------------------------ /v2/tags/{tag_id} ------------------------ #
    # -------------------------- PUT 修改标签 ---------------------------- #
