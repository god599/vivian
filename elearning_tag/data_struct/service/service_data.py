# coding=utf-8

from data_struct.util import *


# -------------------- 请求参数 ------------------------ #
class ExpressParamData(BaseData):
    """
    快递参数
    """
    def __init__(self, type=None, postid=None):
        """
        type	       string        	    required	资源标识
        postid	       string               optional	标签标识列表
        """
        BaseData.__init__(self)
        self.params = copy_dict(locals())

class WordParamData(BaseData):
    """
    单词参数
    """
    def __init__(self, q=None, num=None, doctype=None):
        """
        q	       string        	    required	关键字
        num	       int                  optional	单词个数，默认5各
        doctype	   string               optional	返回格式，默认xml
        """
        BaseData.__init__(self)
        self.params = copy_dict(locals())

class ResourceTagParamData(BaseData):
    """
    资源标签
    """
    def __init__(self, resource_id=None, tag_ids=None):
        """
        resource_id	       string        	    required	资源标识
        tag_ids	           array[string]        optional	标签标识列表
        """
        BaseData.__init__(self)
        self.params = copy_dict(locals())


class SearchResourceTagData(BaseData):
    """
    相关参数查询
    """
    def __init__(self, filter=None, order=None, offset=None, limit=None, result=None, select=None):
        """
        查询语法参考gql
        """
        BaseData.__init__(self)
        self.params = copy_dict(locals())


class ResourceTagData(BaseData):
    """
    资源标签domain
    """
    def __init__(self, id=None, resource_id=None, tag_id=None, create_time=None, create_user=None,
                 custom_id=None, custom_type=None):
        """
        id                 string (uuid)    	optional	  标识
        resource_id	       string        	    optional	  资源标识
        tag_id	           string (uuid)        optional	  标签标识
        create_time        string (date-time)   optional	  创建时间
        create_user	       integer (int64)    	optional	  创建用户的标识
        custom_id	       string               optional	  自定义ID
        custom_type	       string               optional	  自定义类型
        """
        BaseData.__init__(self)
        self.params = copy_dict(locals())


class TagData(BaseData):
    """
    标签
    """
    def __init__(self, id=None, title=None, parent_id=None, sort_number=None, create_time=None, create_user_id=None,
                 update_time=None, update_user_id=None, project_id=None, custom_id=None, custom_type=None,
                 app_store_object_id=None):
        """
        id	                   string (uuid)	    optional	标签标识（只读）
        title	               string               required	标签名称
        parent_id	           string (uuid)	    optional	父标签标识
        sort_number	           integer (int32)	    optional	排序号
        create_time	           string (date-time) 	optional	创建时间（只读）
        create_user_id	       integer (int64)      optional	创建用户的标识（只读）
        update_time	           string (date-time)   optional	更新时间（只读）
        update_user_id	       integer (int64)      optional	更新用户的标识（只读）
        project_id	           integer (int64)	    optional	项目标识(创建、修改时，无需传值)
        custom_id	           string       	    optional	自定义ID
        custom_type	           string	            optional	自定义类型
        app_store_object_id	   string (uuid) 	    optional	app图片id
        """
        BaseData.__init__(self)
        self.params = copy_dict(locals())


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


class TagTreeCustomParameter(BaseData):
    """
    查询标签树(无排序)的参数
    """

    def __init__(self, custom_id=None, custom_type=None):
        """
        custom_id	       string         optional	    自定义custom_id
        custom_type	       boolean        optional	    自定义类型
        """
        BaseData.__init__(self)
        self.params = copy_dict(locals())


class TagVoData(BaseData):
    """
    标签
    """
    def __init__(self, id=None, title=None, parent_id=None, sort_number=None, create_time=None, create_user_id=None,
                 update_time=None, update_user_id=None, project_id=None, custom_id=None, custom_type=None,
                 app_store_object_id=None):
        """
        id	                   string (uuid)	    optional	标签标识（只读）
        title	               string               required	标签名称
        parent_id	           string (uuid)	    optional	父标签标识
        sort_number	           integer (int32)	    optional	排序号
        create_time	           string (date-time) 	optional	创建时间（只读）
        create_user_id	       integer (int64)      optional	创建用户的标识（只读）
        update_time	           string (date-time)   optional	更新时间（只读）
        update_user_id	       integer (int64)      optional	更新用户的标识（只读）
        project_id	           integer (int64)	    optional	项目标识(创建、修改时，无需传值)
        custom_id	           string       	    optional	自定义ID
        custom_type	           string	            optional	自定义类型
        app_store_object_id	   string (uuid) 	    optional	app图片id
        """
        BaseData.__init__(self)
        self.params = copy_dict(locals())


class TagTreeVoData(BaseData):
    """
    标签树
    """
    def __init__(self, id=None, title=None, parent_id=None, sort_number=None, children=None, custom_type=None,
                 custom_id=None, app_store_object_id=None, app_store_object_url=None):
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
        BaseData.__init__(self)
        self.params = copy_dict(locals())


class TagMoveParamData(BaseData):
    """
    标签移动参数
    """
    def __init__(self, parent_id=None, sort_number=None):
        """
        parent_id	       string (uuid)          required	  父标签标识
        sort_number	       integer (int32)        required	  排序号
        """
        BaseData.__init__(self)
        self.params = copy_dict(locals())


# ----------------------- 返回值 ----------------------------- #
class ResourceTag(BaseData):
    """
    资源标签domain
    """
    def __init__(self, data):
        """
        id                 string (uuid)    	optional	  标识
        resource_id	       string        	    optional	  资源标识
        tag_id	           string (uuid)        optional	  标签标识
        create_time        string (date-time)   optional	  创建时间
        create_user	       integer (int64)    	optional	  创建用户的标识
        custom_id	       string               optional	  自定义ID
        custom_type	       string               optional	  自定义类型
        """
        # 1.复制数据
        self.params = data
        assert_that(data, has_key('id'))
        assert_that(data, has_key('resource_id'))
        assert_that(data, has_key('tag_id'))
        assert_that(data, has_key('create_time'))
        assert_that(data, has_key('create_user'))
        assert_that(data, has_key('custom_id'))
        assert_that(data, has_key('custom_type'))


class TagVo(BaseData):
    """
    标签
    """
    def __init__(self, data):
        """
        id	                    string (uuid)	    optional	标签标识
        title	                string	            required	标签名称
        parent_id	            string (uuid)	    optional	父标签标识
        sort_number	            integer (int32)	    optional	排序号(创建修改时，无需传值，通过移动接口修改)
        create_time	            string (date-time)	optional	创建时间（只读）
        create_user_id	        integer (int64)	    optional	创建用户的标识（只读）
        update_time	            string (date-time)	optional	更新时间（只读）
        update_user_id	        integer (int64)	    optional	更新用户的标识
        project_id	            integer (int64)	    optional	项目标识(创建、修改时，无需传值)
        custom_type	            string	            optional	自定义类型
        custom_id	            string	            optional	自定义ID
        app_store_object_id	    string (uuid)	    optional	app图片id
        app_store_object_url	string	            optional	app图片url
        """
        # 1.复制数据
        self.params = data
        assert_that(data, has_key('id'))
        assert_that(data, has_key('title'))
        assert_that(data, has_key('parent_id'))
        assert_that(data, has_key('sort_number'))
        assert_that(data, has_key('create_time'))
        assert_that(data, has_key('create_user_id'))
        assert_that(data, has_key('update_time'))
        assert_that(data, has_key('update_user_id'))
        assert_that(data, has_key('project_id'))
        assert_that(data, has_key('custom_type'))
        assert_that(data, has_key('custom_id'))
        assert_that(data, has_key('app_store_object_id'))
        assert_that(data, has_key('app_store_object_url'))


class TagTreeVo(BaseData):
    """
    标签树
    """
    def __init__(self, data):
        """
        id	                    string (uuid)	    optional	标签标识
        title	                string	            required	标签名称
        parent_id	            string (uuid)	    optional	父标签标识
        sort_number	            integer (int32)	    optional	排序号
        children	            array[TagTreeVo]	optional	子节点
        custom_type	            string	            optional	自定义类型
        custom_id	            string	            optional	自定义ID
        app_store_object_id	    string (uuid)	    optional	app图片id
        app_store_object_url	string	            optional	app图片url

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


class Tag(BaseData):
    """
    标签
    """
    def __init__(self, data):
        """
        id	                string (uuid)	    optional	标签标识（只读）
        title	            string	            required	标签名称
        parent_id	        string (uuid)	    optional	父标签标识
        sort_number	        integer (int32)	    optional	排序号
        create_time	        string (date-time)	optional	创建时间（只读）
        create_user_id	    integer (int64)	    optional	创建用户的标识（只读）
        update_time	        string (date-time)	optional	更新时间（只读）
        update_user_id	    integer (int64)	    optional	更新用户的标识（只读）
        project_id	        integer (int64)	    optional	项目标识(创建、修改时，无需传值)
        custom_id	        string	            optional	自定义ID
        custom_type	        string	            optional	自定义类型
        app_store_object_id	string (uuid)	    optional	app图片id
        """
        # 1.复制数据
        self.params = data
        assert_that(data, has_key('id'))
        assert_that(data, has_key('title'))
        assert_that(data, has_key('parent_id'))
        assert_that(data, has_key('sort_number'))
        assert_that(data, has_key('create_time'))
        assert_that(data, has_key('create_user_id'))
        assert_that(data, has_key('update_time'))
        assert_that(data, has_key('update_user_id'))
        assert_that(data, has_key('project_id'))
        assert_that(data, has_key('custom_type'))
        assert_that(data, has_key('custom_id'))
        assert_that(data, has_key('app_store_object_id'))
