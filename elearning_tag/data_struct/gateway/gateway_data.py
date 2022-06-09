# coding=utf-8

"""

"""

from data_struct.util import *


# ----------------------- 请求参数 ----------------------------- #
class TagTreeParameter(BaseData):
    """
    标签树
    """
    def __init__(self, custom_type=None, need_photo_url=None):
        """
        custom_type	                   string       	    optional	标签标识
        need_photo_url	               boolean        	    required	标签名称
        """
        BaseData.__init__(self)
        self.params = copy_dict(locals())


# ----------------------- 返回值 ----------------------------- #
class TagTreeData(BaseData):
    """
    标签树
    """
    def __init__(self, data):
        """
        id	                   string (uuid)	    optional	标签标识
        title	               string        	    required	标签名称
        parent_id	           string (uuid)        optional	父标签标识
        sort_number	           integer (int32)      optional	排序号
        children	           array[TagTreeVo]     optional	子节点
        custom_type	           string	            optional	自定义类型
        custom_id	           string       	    optional	自定义ID
        app_store_object_id	   string (uuid)	    optional	app图片id
        app_store_object_url   string       	    optional	app图片url
        """
        # 1.复制数据
        self.params = data
        assert_that(data, has_key('id'))
        assert_that(data, has_key('title'))
        assert_that(data, has_key('parent_id'))
        assert_that(data, has_key('sort_number'))
        assert_that(data, has_key('children'))
        assert_that(data, has_key('custom_type'))
        assert_that(data, has_key('custom_id'))
        assert_that(data, has_key('app_store_object_id'))
        assert_that(data, has_key('app_store_object_url'))

