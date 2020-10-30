# -*- codeing = utf-8 -*-
# @Time : 2020/10/27 23:41
# @Author : Cj
# @File : test2.py.py
# @Software : PyCharm

from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from db import MysqlPool

if __name__ == "__main__":
    mp = MysqlPool()
    sql = "select * from tb_review_task"
    s_list = mp.fetch_all(sql,None)
    for s in s_list:
        asins = str(s['asin']).split("|")
        for asin in asins:
            in_sql = "insert into tb_task_asin(task_id,asin,status) values(%s,%s,1)"
            param = [s['id'],asin]
            mp.insert(in_sql,param)