# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import time
import uuid
import pprint
import unittest
from hamcrest import *
from unittest import SkipTest
from nd.rest.rand import CoRand
from nd.rest.restful import Restful


__author__ = "Administrator"  # 开发

#
# 整个工程使用的一套环境代号请保持一致！
#

# 开发
DEV = "dev"
# 测试
TEST = "test"
# 测试2
TEST100 = "test100"
# 预生产
PRE = "pre"
# 生产
OL = "ol"
# AWS
AWS = "aws"
# AWSCA
AWSCA = "awsca"
# WJT（大教育部署）
WJT = "wjt"

# 测试快递
EXP = 'exp_pre'

# 测试快递
WOR = 'word_pre'

# 本地调试代码时使用的环境
# ENVIRONMENT = TEST
# ENVIRONMENT = PRE
# ENVIRONMENT = OL
# ENVIRONMENT = WJT
ENVIRONMENT = WOR
