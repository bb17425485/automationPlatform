# -*- codeing = utf-8 -*-
# @Time : 2020/9/25 16:55
# @Author : Cj
# @File : zzz.py
# @Software : PyCharm

from db import MysqlPool
import random,string,configparser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent

import time
import threading
a = 5

class DownThread:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            global a
            a = 6
            print(a)
            print('T-minus', n)
            n -= 1
            time.sleep(1)


if __name__ == '__main__':
    c = DownThread()
    t = threading.Thread(target=c.run, args=(10,))
    t.start()
    time.sleep(3)
    c.terminate()
    t.join()
    t.is_alive()






    # ua = UserAgent()
    # print(ua.chrome)
    # options = webdriver.ChromeOptions()
    # options.add_argument("user-agent=" + ua.chrome)
    # options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    # driver = webdriver.Chrome(options=options)
    # driver.get("https://www.cashbackbase.com/account/login")
    # # print(driver.find_element_by_xpath('//a[@class="mnav c-font-normal c-color-t"][2]').text)
    # sleep(1)
    # driver.find_element_by_id('email').send_keys('gogogo7@aliyun.com')
    # driver.find_element_by_id('password').send_keys('cuijie1003')
    # driver.find_element_by_id('password').send_keys(Keys.ENTER)
    # sleep(3)
    # print(driver.get_cookies())
    # driver.quit()



    # config = configparser.RawConfigParser()
    # config.read("group-answer.ini", encoding="utf-8")
    # print(config.sections())
    # for group in config:
    #     if r'Coupons, Codes, Deals, Krazy Glitches & Steals!!' == group:
    #         print(len(config[group]['a2']))
