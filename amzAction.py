# -*- codeing = utf-8 -*-
# @Time : 2020/10/1 19:39
# @Author : Cj
# @File : amzAction.py
# @Software : PyCharm

from selenium import webdriver
from time import sleep
import time
import configparser,random,threading,traceback
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random,string
from selenium.webdriver.common.keys import Keys
import win32api,win32con

desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

if __name__ == "__main__":

    config = configparser.RawConfigParser()
    config.read("amz-account.ini", encoding="utf-8")
    for i, account in enumerate(config):
        if i == 1:
            print(account)
            options = webdriver.ChromeOptions()
            options.add_argument("user-agent=" + str(config[account]['ua']))
            options.add_argument("--start-maximized")
            options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
            driver.get("https://www.baidu.com/")
            sleep(1)
            for cookie in eval(config[account]['cookies']):
                driver.add_cookie(cookie_dict=cookie)
            sleep(1)
            # keywords = ["cigarette holder","Garden Plant Trellis","Trellis Net"]
            # keyword = keywords[random.randint(0,2)]
            keyword = "Garden Plant Trellis Net"
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            driver.get("https://www.amazon.com/s?k=" + keyword + "&ref=nb_sb_noss")
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            driver.quit()









            # a1 = random.randint(5,10)
            # sleep(a1)
            # for j in range(random.randint(3,12)):
            #     driver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
            #     sleep(random.randint(1, 4))
            #     if j == 5 or j == 9:
            #         driver.find_element_by_xpath('//body').send_keys(Keys.PAGE_UP)
            #         sleep(random.randint(1, 3))
            # # ActionChains(driver).move_by_offset(random.randint(200,300), random.randint(150,250)).click().perform()
            # print("click")
            # ActionChains(driver).move_by_offset(random.randint(500,800), random.randint(300,400)).click().perform()
            # # print(driver.get_window_size())
            # sleep(random.randint(2,5))
            # for k in range(random.randint(3,9)):
            #     driver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
            #     sleep(random.randint(2, 5))
            #     if k == 5:
            #         driver.find_element_by_xpath('//body').send_keys(Keys.PAGE_UP)
            #         sleep(random.randint(1, 3))
            # driver.quit()

