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

    # ---------------------- /v1/resources/tags ----------------------- #
    # ----------------------- PUT 设置资源标签 ------------------------- #
    def test_put_resources_tags(self):
        """
        传入存在的resource_id，设置资源标签
        【done】
        level:1,2,3,4,5,6,7
        """
        # 查询资源标签，获取现有的资源标识resource_id ————避免出现资源id不存在的情况
        search_url = SearchResourceTagData()
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")
        resource_id = data_dict['items'][0]['resource_id']

        # 根据查询resource_id，设置资源标签
        resource_tag_param = ResourceTagParamData(resource_id=resource_id)
        res = self.tag_o.set_resources_tags(resource_tag_param)
        data_dict1 = self.rest_o.parse_response(res, OK, '设置资源标签失败')

        # 查询的标签中有设置的标签
        search_url = SearchResourceTagData()
        res = self.tag_o.search_tags_tree(search_url)
        self.rest_o.parse_response(res, OK, "查询资源标签失败")

        assert_that(data_dict1, is_({}))

    def test_put_wrong_resources_tags(self):
        """
        传入不存在的resource_id，设置资源标签
        【done】
        level:1,3,5
        """
        # 传入不存在的resource_id（格式正确），设置资源标签
        resource_tag_param = ResourceTagParamData(resource_id='28d57634-dd64-4f81-a3fd-6cde44012345')
        res = self.tag_o.set_resources_tags(resource_tag_param)
        # 成功
        self.rest_o.parse_response(res, OK, '设置资源标签成功')

        # 传入不存在的resource_id（格式错误），设置资源标签
        resource_tag_param = ResourceTagParamData(resource_id='28d57635')
        res = self.tag_o.set_resources_tags(resource_tag_param)
        # 失败
        self.rest_o.parse_response(res, OK, '设置资源标签成功')

    def test_put_no_resources_tags(self):
        """
        不传入resource_id，设置资源标签
        【done】
        level:1,3,5
        """
        resource_tag_param = ResourceTagParamData()
        res = self.tag_o.set_resources_tags(resource_tag_param)
        # 提建议
        self.rest_o.parse_response(res, 500, '设置资源标签成功')

    # --------------------- /v1/resources/tags/search ------------------------ #
    # -------------------------- GET 查询资源标签 ----------------------------- #

    def test_get_resources_tags_no_use_parameter(self):
        """
        选填：$filter、$order、$offset、$limit、$result、$select，参数均不传，查询资源标签
        【done】
        level:1,2,3,4,5,6,7
        """
        # 不传参数
        search_url = SearchResourceTagData()
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")
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
        search_url = SearchResourceTagData()
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")
        tag_id = data_dict['items'][0]['id']

        filter = 'id eq ' + str(tag_id)
        search_url = SearchResourceTagData(filter=filter)
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

    def test_get_resources_tags_use_wrong_filter(self):
        """
        $filter（其他参数不传）
        $filter = 不正确的取值，如：$filter = id eq abc，查询资源标签
        【done】
        level:1,3,5
        """
        # 使用查询标签树，查询存在的id（标签标识）
        filter = 'id eq abc'
        search_url = SearchResourceTagData(filter=filter)
        res = self.tag_o.get_search_resources_tags(search_url)
        self.rest_o.parse_response(res, 400, "查询资源标签失败")

    def test_get_resources_tags_use_order_create_time_asc(self):
        """
        $order（其他参数不传）
        $order = 正确的取值，$order = create_time asc（递增），查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        search_url = SearchResourceTagData(order='create_time asc')
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")
        if len(data_dict['items']) > 2:
            assert_that(data_dict['items'][0]['create_time'] <= data_dict['items'][1]['create_time'], is_(True))
            assert_that(data_dict['items'][1]['create_time'] <= data_dict['items'][2]['create_time'], is_(True))

    def test_get_resources_tags_use_order_create_time_desc(self):
        """
        $order（其他参数不传）
        $order = 正确的取值，$order = create_time desc（递减），查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        search_url = SearchResourceTagData(order='create_time desc')
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")
        if len(data_dict['items']) > 2:
            assert_that(data_dict['items'][0]['create_time'] >= data_dict['items'][1]['create_time'], is_(True))
            assert_that(data_dict['items'][1]['create_time'] >= data_dict['items'][2]['create_time'], is_(True))

    def test_get_resources_tags_use_offset1(self):
        """
        $offset（其他参数不传）
        $offset=0（默认值），查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        # offset=0（默认值）获取一次
        search_url = SearchResourceTagData(offset=0)
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 不传任何参数，获取一次
        search_url = SearchResourceTagData()
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 两次返回的结果一致
        assert_that(data_dict, is_(data_dict1))

    def test_get_resources_tags_use_offset2(self):
        """
        $offset（其他参数不传）
        $offset=2 ，查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        # offset=2，获取一次
        search_url = SearchResourceTagData(offset=2)
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 不传任何参数，获取一次
        search_url = SearchResourceTagData(offset=0)
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 第二次返回的结果为，第一次返回的结果中的第3个元素开始
        if len(data_dict['items']) > 1:
            assert_that(data_dict['items'][0], is_(data_dict1['items'][2]))

    def test_get_resources_tags_use_wrong_offset(self):
        """
        $offset（其他参数不传）
        $offset=-1(错误值) ，查询资源标签
        【done】
        level:1,3,5
        """
        # offset=-1，获取一次
        search_url = SearchResourceTagData(offset=-1)
        res = self.tag_o.get_search_resources_tags(search_url)
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询资源标签失败")

    def test_get_resources_tags_use_limit1(self):
        """
        $limit（其他参数不传）
        $limit=20（默认值），查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        # limit=20（默认值）获取一次
        search_url = SearchResourceTagData(limit=20)
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 不传任何参数，获取一次
        search_url = SearchResourceTagData()
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 两次返回的结果一致
        assert_that(data_dict, is_(data_dict1))

    def test_get_resources_tags_use_limit2(self):
        """
        $limit（其他参数不传）
        $limit=10 ，查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        # limit=10 获取一次
        search_url = SearchResourceTagData(limit=10)
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 不传任何参数，获取一次
        search_url = SearchResourceTagData()
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询资源标签失败")
        data_dict2 = data_dict1['items'][:10]

        # 第二次结果返回10条，返回数据是默认值的前10条
        assert_that(data_dict['items'][:], is_(data_dict2))

    def test_get_resources_tags_use_wrong_limit(self):
        """
        $limit（其他参数不传）
        $limit=-1（错误值） ，查询资源标签
        【done】
        level:1,3,5
        """
        # limit=-1（错误值） 获取一次
        search_url = SearchResourceTagData(limit=-1)
        res = self.tag_o.get_search_resources_tags(search_url)
        self.rest_o.parse_response(res, 400, "查询资源标签失败")

    def test_get_resources_tags_use_result_equal_to_list(self):
        """
        $result（其他参数不传）
        $result=list ，查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        # result=list ，查询资源标签
        search_url = SearchResourceTagData(result='list')
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 两次返回的total=null和items
        assert_that(data_dict['total'], is_(None))
        assert_that(data_dict['items'], is_not(None))

    def test_get_resources_tags_use_result_equal_to_pager(self):
        """
        $result（其他参数不传）
        $result=pager ，查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        # result=pager ，查询资源标签
        search_url = SearchResourceTagData(result='pager')
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 两次返回的total和items
        assert_that(data_dict['total'], is_not(None))
        assert_that(data_dict['items'], is_not(None))

    def test_get_resources_tags_use_result_equal_to_count(self):
        """
        $result（其他参数不传）
        $result=count ，查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        # result=count ，查询资源标签
        search_url = SearchResourceTagData(result='count')
        res = self.tag_o.get_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 两次返回的total和items
        assert_that(data_dict['total'], is_not(None))
        assert_that(data_dict['items'], is_(None))

    def test_get_resources_tags_use_wrong_result(self):
        """
        $result（其他参数不传）
        $result=不正确的取值，如：$result=count1 ，查询资源标签
        【done】
        level:1,3,5
        """
        # result=count ，查询资源标签
        search_url = SearchResourceTagData(result='count1')
        res = self.tag_o.get_search_resources_tags(search_url)
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询资源标签失败")

    def test_get_resources_tags_use_select_equal_to_resource_id(self):
        """
        $select（其他参数不传）
        $select=resource_id，查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        # select=resource_id，查询资源标签
        search_url = SearchResourceTagData(select='resource_id')
        res = self.tag_o.get_search_resources_tags(search_url)
        self.rest_o.parse_response(res, OK, "查询资源标签失败")

    def test_get_resources_tags_use_wrong_select(self):
        """
        $select（其他参数不传）
        $select=不正确的取值，如：$select=name，查询资源标签
        【done】
        level:1,3,5
        """
        # select=resource_id，查询资源标签
        search_url = SearchResourceTagData(select='name')
        res = self.tag_o.get_search_resources_tags(search_url)
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询资源标签失败")

    # --------------------- /v1/resources/tags/search ------------------------ #
    # ------------------------- POST 查询资源标签 ----------------------------- #
    def test_post_resources_tags_no_use_parameter(self):
        """
        选填：$filter、$order、$offset、$limit、$result、$select，参数均不传，查询资源标签
        【done】
        level:1,2,3,4,5,6,7
        """
        # 不传参数
        search_url = SearchResourceTagData()
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")
        if data_dict:
            for i in data_dict['items']:
                ResourceTag(i)

    def test_post_resources_tags_use_filter(self):
        """
        $filter（其他参数不传）
        $filter = 正确的取值，如：$filter = tag_id eq xxx（标签标识），查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        # 使用查询标签树，查询存在的id（标签标识）
        search_url = SearchResourceTagData()
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")
        tag_id = data_dict['items'][0]['id']

        filter = 'id eq ' + str(tag_id)
        search_url = SearchResourceTagData(filter=filter)
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        ResourceTag(data_dict1['items'][0])
        assert_that(data_dict1['items'][0]['id'], equal_to(tag_id))

    def test_post_resources_tags_use_none_filter(self):
        """
        $filter（其他参数不传）
        传入空$filter串，查询资源标签
        【done】
        level:1,3,5
        """
        search_url = SearchResourceTagData(filter='')
        res = self.tag_o.post_search_resources_tags(search_url)
        self.rest_o.parse_response(res, OK, "查询资源标签失败")

    def test_post_resources_tags_use_wrong_filter(self):
        """
        $filter（其他参数不传）
        $filter = 不正确的取值，如：$filter = id eq abc，查询资源标签
        【done】
        level:1,3,5
        """
        # 使用查询标签树，查询存在的id（标签标识）
        filter = 'id eq abc'
        search_url = SearchResourceTagData(filter=filter)
        res = self.tag_o.post_search_resources_tags(search_url)
        self.rest_o.parse_response(res, 400, "查询资源标签失败")

    def test_post_resources_tags_use_order_create_time_asc(self):
        """
        $order（其他参数不传）
        $order = 正确的取值，$order = create_time asc（递增），查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        search_url = SearchResourceTagData(order='create_time asc')
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")
        if len(data_dict['items']) > 2:
            assert_that(data_dict['items'][0]['create_time'] <= data_dict['items'][1]['create_time'], is_(True))
            assert_that(data_dict['items'][1]['create_time'] <= data_dict['items'][2]['create_time'], is_(True))

    def test_post_resources_tags_use_order_create_time_desc(self):
        """
        $order（其他参数不传）
        $order = 正确的取值，$order = create_time desc（递减），查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        search_url = SearchResourceTagData(order='create_time desc')
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")
        if len(data_dict['items']) > 2:
            assert_that(data_dict['items'][0]['create_time'] >= data_dict['items'][1]['create_time'], is_(True))
            assert_that(data_dict['items'][1]['create_time'] >= data_dict['items'][2]['create_time'], is_(True))

    def test_post_resources_tags_use_offset1(self):
        """
        $offset（其他参数不传）
        $offset=0（默认值），查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        # offset=0（默认值）获取一次
        search_url = SearchResourceTagData(offset=0)
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 不传任何参数，获取一次
        search_url = SearchResourceTagData()
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 两次返回的结果一致
        assert_that(data_dict, is_(data_dict1))

    def test_post_resources_tags_use_offset2(self):
        """
        $offset（其他参数不传）
        $offset=2 ，查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        # offset=2，获取一次
        search_url = SearchResourceTagData(offset=2)
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 不传任何参数，获取一次
        search_url = SearchResourceTagData(offset=0)
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 第二次返回的结果为，第一次返回的结果中的第3个元素开始
        if len(data_dict['items']) > 1:
            assert_that(data_dict['items'][0], is_(data_dict1['items'][2]))

    def test_post_resources_tags_use_wrong_offset(self):
        """
        $offset（其他参数不传）
        $offset=-1(错误值) ，查询资源标签
        【done】
        level:1,3,5
        """
        # offset=-1，获取一次
        search_url = SearchResourceTagData(offset=-1)
        res = self.tag_o.post_search_resources_tags(search_url)
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询资源标签失败")

    def test_post_resources_tags_use_limit1(self):
        """
        $limit（其他参数不传）
        $limit=20（默认值），查询资源标签
        【done】
        level:1,2,3,4,5,6
        """
        # limit=20（默认值）获取一次
        search_url = SearchResourceTagData(limit=20)
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 不传任何参数，获取一次
        search_url = SearchResourceTagData()
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 两次返回的结果一致
        assert_that(data_dict, is_(data_dict1))

    def test_post_resources_tags_use_limit2(self):
        """
        $limit（其他参数不传）
        $limit=10 ，查询资源标签
        【done】
        level:1,2,3,4,5
        """
        # limit=10 获取一次
        search_url = SearchResourceTagData(limit=10)
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 不传任何参数，获取一次
        search_url = SearchResourceTagData()
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询资源标签失败")
        data_dict2 = data_dict1['items'][:10]

        # 第二次结果返回10条，返回数据是默认值的前10条
        assert_that(data_dict['items'][:], is_(data_dict2))

    def test_post_resources_tags_use_wrong_limit(self):
        """
        $limit（其他参数不传）
        $limit=-1（错误值） ，查询资源标签
        【done】
        level:1,3,5
        """
        # limit=-1（错误值） 获取一次
        search_url = SearchResourceTagData(limit=-1)
        res = self.tag_o.post_search_resources_tags(search_url)
        self.rest_o.parse_response(res, 400, "查询资源标签失败")

    def test_post_resources_tags_use_result_equal_to_list(self):
        """
        $result（其他参数不传）
        $result=list ，查询资源标签
        【done】
        level:1,2,3,4
        """
        # result=list ，查询资源标签
        search_url = SearchResourceTagData(result='list')
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 两次返回的total=null和items
        assert_that(data_dict['total'], is_(None))
        assert_that(data_dict['items'], is_not(None))

    def test_post_resources_tags_use_result_equal_to_pager(self):
        """
        $result（其他参数不传）
        $result=pager ，查询资源标签
        【done】
        level:1,2,3,4,5
        """
        # result=pager ，查询资源标签
        search_url = SearchResourceTagData(result='pager')
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 两次返回的total和items
        assert_that(data_dict['total'], is_not(None))
        assert_that(data_dict['items'], is_not(None))

    def test_post_resources_tags_use_result_equal_to_count(self):
        """
        $result（其他参数不传）
        $result=count ，查询资源标签
        【done】
        level:1,2,3,4,5
        """
        # result=count ，查询资源标签
        search_url = SearchResourceTagData(result='count')
        res = self.tag_o.post_search_resources_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询资源标签失败")

        # 两次返回的total和items
        assert_that(data_dict['total'], is_not(None))
        assert_that(data_dict['items'], is_(None))

    def test_post_resources_tags_use_wrong_result(self):
        """
        $result（其他参数不传）
        $result=不正确的取值，如：$result=count1 ，查询资源标签
        【done】
        level:1,3,5
        """
        # result=count ，查询资源标签
        search_url = SearchResourceTagData(result='count1')
        res = self.tag_o.post_search_resources_tags(search_url)
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询资源标签失败")

    def test_post_resources_tags_use_select_equal_to_resource_id(self):
        """
        $select（其他参数不传）
        $select=resource_id，查询资源标签
        【done】
        level:1,2,3,4,5
        """
        # select=resource_id，查询资源标签
        search_url = SearchResourceTagData(select='resource_id')
        res = self.tag_o.post_search_resources_tags(search_url)
        self.rest_o.parse_response(res, OK, "查询资源标签失败")

    def test_post_resources_tags_use_wrong_select(self):
        """
        $select（其他参数不传）
        $select=不正确的取值，如：$select=name，查询资源标签
        【done】
        level:1,3,5
        """
        # select=resource_id，查询资源标签
        search_url = SearchResourceTagData(select='name')
        res = self.tag_o.post_search_resources_tags(search_url)
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询资源标签失败")

    # ------------------------ /v1/tags ------------------------ #
    # ---------------------- GET 查询标签 ------------------------ #
    # 传入存在的标签标识，查询标签 --------在创建标签中覆盖

    def test_search_tags_use_wrong_params(self):
        """
        传入不存在的标签标识，查询标签
        【done】
        level:1,3,5
        """
        # 传入不存在的标签标识（格式正确），查询标签
        res = self.tag_o.search_tags(tag_ids='1f01f0df-af7f-4396-8355-e1234b912342')
        # 成功，返回数据为空
        data_dict = self.rest_o.parse_response(res, OK, "查询标签失败")
        assert_that(data_dict, equal_to([]))

        # 传入不存在的标签标识（格式错误），查询标签
        res = self.tag_o.search_tags(tag_ids='1232455454')
        # 失败
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询标签失败")

    def test_search_tags_no_use_params(self):
        """
        不传入标签标识，查询标签
        【done】
        level:1,3,5
        """
        res = self.tag_o.search_tags(tag_ids=None)
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询标签失败")

    # ------------------------ /v1/tags ------------------------- #
    # ---------------------- POST 创建标签 ----------------------- #
    def test_add_tags_pass_title(self):
        """
        传入title，创建标签
        【done】
        level:1,2,3,4,5,6,7
        """
        # 传入title，创建标签
        title = 'api_标签名称' + self.rand_o.randomword(5)
        search_url = TagData(title=title)
        res = self.tag_o.add_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "创建标签失败")
        TagVo(data_dict)
        tag_id = data_dict['id']
        self.tag_id_list.append(tag_id)

        # 查询标签
        res = self.tag_o.search_tags(tag_id)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询标签失败")
        TagVo(data_dict)
        assert_that(data_dict1[0]['title'], equal_to(title))

        # 删除标签
        res = self.tag_o.delete_tags(tag_id=tag_id)
        self.rest_o.parse_response(res, OK, "删除标签失败")
        self.tag_id_list = []
        TagVo(data_dict)

    def test_add_tags_no_pass_title(self):
        """
        不传入title，创建标签
        【done】
        level:1,3,5
        """
        # 不传入title，创建标签
        search_url = TagData()
        res = self.tag_o.add_tags(search_url)
        # 500，提建议
        self.rest_o.parse_response(res, 500, "创建标签失败")

    # -------------------- /v1/tags/tree ------------------------ #
    # -------------------- GET 查询标签树 ------------------------ #
    def test_get_tags_tree_no_pass_parameter(self):
        """
        custom_type和need_photo_url为选填项，不传这两个参数，获取标签树
        【done】
        level:1,2,3,4,5,6,7
        """
        search_url = TagTreeParameter()
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "获取标签失败")
        TagTreeVo(data_dict)

    def test_get_tags_tree_pass_custom_type1(self):
        """
        传入存在的custom_type，如：custom_type='el-learning-unit'（资源池标签），不传入need_photo_url，获取标签树
        【done】
        level:1,2,3,4,5
        """
        search_url = TagTreeParameter(custom_type='el-learning-unit')
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "获取标签失败")
        if data_dict:
            TagTreeVo(data_dict)
            assert_that(data_dict, has_key('custom_type'))
            assert_that(data_dict['custom_type'], equal_to('el-learning-unit'))

    def test_get_tags_tree_pass_nonexistent_custom_type(self):
        """
        传入不存在的custom_type，如：custom_type='el-learning-unit1'（资源池标签），不传入need_photo_url，获取标签树
        【done】
        level:1,3,5
        """
        search_url = TagTreeParameter(custom_type='el-learning-unit1')
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "获取标签失败")

        assert_that(data_dict, equal_to({}))

    def test_get_tags_tree_pass_need_photo_url_equal_to_true(self):
        """
        传入need_photo_url参数，need_photo_url为true，不传入custom_type，获取标签树
        【done】
        level:1,3,5
        """
        search_url = TagTreeParameter(need_photo_url='true')
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "获取标签失败")
        TagTreeVo(data_dict)

    def test_get_tags_tree_pass_need_photo_url_equal_to_false(self):
        """
        传入need_photo_url参数，need_photo_url为false，不传入custom_type，获取标签树
        【done】
        level:1,3,5
        """
        search_url = TagTreeParameter(need_photo_url='false')
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "获取标签失败")
        TagTreeVo(data_dict)

    def test_get_tags_tree_pass_need_photo_url(self):
        """
        传入need_photo_url参数，need_photo_url为错误值true1，不传入custom_type，获取标签树
        【done】
        level:1,3,5
        """
        search_url = TagTreeParameter(need_photo_url='true1')
        res = self.tag_o.search_tags_tree(search_url)
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "获取标签失败")

    def test_get_tags_tree_pass_two_parameter(self):
        """
        custom_type和need_photo_url为选填项，传这两个参数，获取标签树
        【done】
        level:1,2,3,4,5
        """
        search_url = TagTreeParameter(custom_type='el-learning-unit', need_photo_url='true')
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "获取标签失败")
        if data_dict:
            TagTreeVo(data_dict)
            assert_that(data_dict['custom_type'], equal_to('el-learning-unit'))

    # ----------------------- /v1/tags/tree/children ------------------------- #
    # -------------------- GET 根据标签标识查询子标签树 ------------------------ #
    def test_search_tags_tree_children_use_params(self):
        """
        传入存在的标签标识，查询子标签树
        【done】
        level:1,3,5,7
        """
        # 查询标签树，获取标签标识
        search_url = TagTreeParameter()
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询子标签树失败")
        tag_id = data_dict['children'][0]['id']

        # 传入存在的标签标识，查询子标签树
        res = self.tag_o.according_to_tag_id_to_search_tags_tree_children(tag_id)
        data_dict = self.rest_o.parse_response(res, OK, "查询子标签树失败")
        TagTreeVo(data_dict)

    def test_search_tags_tree_children_use_wrong_params(self):
        """
        传入不存在的标签标识，查询子标签树
        【done】
        level:1,3,5
        """
        # 传入不存在的标签标识（格式正确），查询标签
        res = self.tag_o.according_to_tag_id_to_search_tags_tree_children(tag_id='1f01f0df-af7f-4396-8355-e1234b912342')

        # 失败（目前报500，已提建议）
        self.rest_o.parse_response(res, 500, "查询子标签树失败")

        # 传入不存在的标签标识（格式错误），查询标签
        res = self.tag_o.according_to_tag_id_to_search_tags_tree_children(tag_id='1232455454')
        # 失败
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询子标签树失败")

    def test_search_tree_children_tags_no_use_params(self):
        """
        不传入标签标识，查询标签
        【done】
        level:1,3,5
        """
        res = self.tag_o.according_to_tag_id_to_search_tags_tree_children(tag_id=None)
        self.rest_o.parse_response(res, REQUIRE_ARGUMENT, "查询子标签树失败")

    # ------------------------ /v1/tags/treewithoutsort ------------------------- #
    # -------------------------- GET 查询标签树(无排序) -------------------------- #
    def test_get_tags_tree_without_sort_no_pass_parameter(self):
        """
        custom_id和custom_type为选填项，不传这两个参数,查询标签树（无排序）
        【done】
        level:1,2,3,4,5,6,7
        """
        search_url = TagTreeCustomParameter()
        res = self.tag_o.search_tags_tree_without_sort(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询标签树失败")
        for i in data_dict:
            Tag(i)

    def test_get_tags_tree_without_sort_pass_custom_id(self):
        """
        传入存在的custom_id，不传入custom_type，查询标签树
        【done】
        level:1,3,5
        """
        # 查询标签树，获取custom_id
        search_url = TagTreeParameter()
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询标签树失败")
        custom_id = data_dict['children'][0]['custom_id']

        search_url = TagTreeCustomParameter(custom_id=custom_id)
        res = self.tag_o.search_tags_tree_without_sort(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询标签树失败")
        Tag(data_dict1[0])
        assert_that(data_dict1[0]['custom_id'], equal_to(custom_id))

    def test_get_tags_tree_without_sort_pass_nonexistent_custom_id(self):
        """
        传入不存在的custom_id，，不传入need_photo_url，查询标签树
        【done】
        level:1,3,5
        """
        search_url = TagTreeCustomParameter(custom_id='custom_id1')
        res = self.tag_o.search_tags_tree_without_sort(search_url)
        self.rest_o.parse_response(res, OK, "查询标签树失败")

        # 查询标签时，若没有标签，该项目存在根节点标签时，返回根节点标签。

    def test_get_tags_tree_without_sort_pass_custom_type(self):
        """
        传入存在的custom_type，不传入custom_id，查询标签树
        【done】
        level:1,3,5
        """
        # 查询标签树，获取custom_type
        search_url = TagTreeParameter()
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询标签树失败")
        custom_type = data_dict['children'][0]['custom_type']

        search_url = TagTreeCustomParameter(custom_type=custom_type)
        res = self.tag_o.search_tags_tree_without_sort(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询标签树失败")
        Tag(data_dict1[0])
        assert_that(data_dict1[0]['custom_type'], equal_to(custom_type))

    def test_get_tags_tree_without_sort_pass_nonexistent_custom_type(self):
        """
        传入不存在的custom_type，不传入custom_id，查询标签树
        【done】
        level:1,3,5
        """
        search_url = TagTreeCustomParameter(custom_type='el-channel1')
        res = self.tag_o.search_tags_tree_without_sort(search_url)
        self.rest_o.parse_response(res, OK, "查询标签树失败")

    def test_get_tags_tree_without_sort_pass_two_parameter(self):
        """
        custom_type和custom_id为选填项，传这两个参数，搜索标签树
        【done】
        level:1,3,5
        """
        # 查询标签树，获取custom_type和custom_id
        search_url = TagTreeParameter()
        res = self.tag_o.search_tags_tree(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "查询标签树失败")
        custom_id = data_dict['children'][0]['custom_id']
        custom_type = data_dict['children'][0]['custom_type']

        search_url = TagTreeCustomParameter(custom_id=custom_id, custom_type=custom_type)
        res = self.tag_o.search_tags_tree_without_sort(search_url)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询标签树失败")
        Tag(data_dict1[0])
        assert_that(data_dict1[0]['custom_id'], equal_to(custom_id))
        assert_that(data_dict1[0]['custom_type'], equal_to(custom_type))

    # ------------------------ /v1/tags/{tag_id} ------------------------ #
    # -------------------------- GET 查询标签 ---------------------------- #
    def test_search_tags_use_url(self):
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
        res = self.tag_o.search_tags_id(tag_id)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询标签失败")

        assert_that(data_dict1['id'], equal_to(tag_id))

    def test_search_tags_use_wrong_url(self):
        """
        传入不存在的标签标识，查询标签
        【done】
        level:1,3,5
        """
        # 传入不存在的标签标识（格式正确），查询标签
        res = self.tag_o.search_tags_id(tag_id='5f543ae7-b489-4ada-a1ae-dd34dbe3a123')
        # 成功，返回数据为空
        data_dict = self.rest_o.parse_response(res, OK, "查询标签失败")
        assert_that(data_dict, equal_to({}))

        # 传入不存在的标签标识（格式错误），查询标签
        res = self.tag_o.search_tags_id(tag_id='1232455454')
        # 失败
        self.rest_o.parse_response(res, INVALID_ARGUMENT, "查询标签失败")

    # ------------------------ /v1/tags/{tag_id} ------------------------ #
    # -------------------------- PUT 修改标签 ---------------------------- #

    # --------------------------- /v1/tags/{tag_id} ---------------------------- #
    # ----------------------DELETE 删除标签(与资源关系也删除)--------------------- #
    def test_delete_tags_pass_tag_id(self):
        """
        传入存在的标签标识，删除标签
        【done】
        level:1,2,3,4,5,6,7
        """
        # 传入title，创建标签
        title = 'api_标签名称' + self.rand_o.randomword(5)
        search_url = TagData(title=title)
        res = self.tag_o.add_tags(search_url)
        data_dict = self.rest_o.parse_response(res, OK, "创建标签失败")
        TagVo(data_dict)
        tag_id = data_dict['id']
        self.tag_id_list.append(tag_id)

        # 查询标签
        res = self.tag_o.search_tags_id(tag_id)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询标签失败")
        assert_that(data_dict1['id'], equal_to(tag_id))

        # 删除标签
        res = self.tag_o.delete_tags(tag_id=tag_id)
        self.rest_o.parse_response(res, OK, "删除标签失败")
        self.tag_id_list = []

        # 查询标签
        res = self.tag_o.search_tags_id(tag_id)
        data_dict1 = self.rest_o.parse_response(res, OK, "查询标签失败")
        assert_that(data_dict1, equal_to({}))

    def test_delete_tags_pass_wrong_tag_id(self):
        """
        传入不存在的标签标识，删除标签
        【done】
        level:1,3,5
        """
        # 传入不存在的标签标识（格式正确），删除标签
        res = self.tag_o.delete_tags(tag_id='5f543ae7-b489-4ada-a1ae-dd34dbe3a123')
        self.rest_o.parse_response(res, 404, "删除标签失败")

        # 传入不存在的标签标识（格式错误），删除标签
        res = self.tag_o.delete_tags(tag_id='5f543a')
        self.rest_o.parse_response(res, 400, "删除标签失败")

    # --------------------------- /v1/tags/{tag_id}/move -------------------------- #
    # --------------------------------DELETE 移动标签------------------------------- #