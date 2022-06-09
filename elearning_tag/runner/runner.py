# coding=utf-8
import sys
import os
from nd.rest.co_test.runner import run

__author__ = 'linzh'

reload(sys)

sys.setdefaultencoding('utf-8')

sys.path.insert(0, '..')

run(os.path.realpath(__file__))
