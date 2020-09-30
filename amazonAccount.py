# -*- codeing = utf-8 -*-
# @Time : 2020/9/22 16:08
# @Author : Cj
# @File : amazonAccount.py
# @Software : PyCharm

from selenium import webdriver
from time import sleep
import random,string
from selenium.webdriver.common.keys import Keys
import win32api,win32con

if __name__ == "__main__":
    mobile_emulation = {"deviceName": "Galaxy S5"}
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument(
    #     "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14")
    options.add_experimental_option('mobileEmulation', mobile_emulation)
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.amazon.com')
    driver.find_element_by_xpath('//*[@id="nav-logobar-greeting"]').click()
    sleep(1)
    driver.find_element_by_xpath('//*[@id="register_accordion_header"]').click()
    sleep(1)
    driver.find_element_by_xpath('//*[@id="ap_customer_name"]').send_keys("patt imnny")
    account = "79912094240"
    driver.find_element_by_name('email').send_keys(account)
    src = string.ascii_letters + string.digits
    list_passwd_all = random.sample(src, 7)  # 从字母和数字中随机取5位
    list_passwd_all.extend(random.sample(string.digits, 1))  # 让密码中一定包含数字
    list_passwd_all.extend(random.sample(string.ascii_lowercase, 1))  # 让密码中一定包含小写字母
    list_passwd_all.extend(random.sample(string.ascii_uppercase, 1))  # 让密码中一定包含大写字母
    random.shuffle(list_passwd_all)  # 打乱列表顺序
    str_passwd = ''.join(list_passwd_all)  # 将列表转化为字符串
    driver.find_element_by_name('password').send_keys(str_passwd)
    sleep(1)
    driver.find_element_by_xpath('//*[@id="ap_register_form"]/div[2]/div[1]/div[1]/span/span').click()
    sleep(1)
    # win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,1250)
    # sleep(1)
    driver.find_element_by_xpath('//*[@id="ap-countries-list"]/li[164]').click()
    sleep(1.5)
    driver.find_element_by_xpath('//*[@id="continue"]').click()
    while True:
        sleep(5)
        print(account)
        print(str_passwd)
        print(driver.get_cookies())