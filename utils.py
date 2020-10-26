# -*- codeing = utf-8 -*-
# @Time : 2020/10/22 13:01
# @Author : Cj
# @File : utils.py
# @Software : PyCharm

import hashlib,re

class pyUtils:
    @staticmethod
    def getMd5(string):
        return hashlib.md5(string.encode("utf-8")).hexdigest()

    @staticmethod
    def filter_str(desstr, restr=''):
        # 过滤除中英文及数字及英文标点以外的其他字符
        res = re.compile("[^\u4e00-\u9fa5^. !//_,$&%^*()<>+\"'?@#-|:~{}+|—^a-z^A-Z^0-9]")
        return res.sub(restr, desstr)
