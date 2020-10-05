# -*- codeing = utf-8 -*-
# @Time : 2020/10/4 1:21
# @Author : Cj
# @File : cashBackBase.py
# @Software : PyCharm

from selenium import webdriver
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from db import MysqlPool
import traceback

def getData():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.baidu.com/")
    cookies = [{'domain': '.cashbackbase.com', 'expiry': 1599363219, 'httpOnly': False, 'name': '_gat_gtag_UA_119767146_3', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.cashbackbase.com', 'expiry': 1757043117, 'httpOnly': True, 'name': 'cash-ab-test', 'path': '/', 'secure': False, 'value': 'eyJpdiI6InFRZHJVdDNYUHA0UXpPell2MFZFM2c9PSIsInZhbHVlIjoieXFZSjRManpHb00zR01vaGpiNlY5Zz09IiwibWFjIjoiMDU5ZGY3YjA3OGVlNjM2MWRhMjk1YmIxNDJiZTNhOTkxMzRkN2UzNGVhYzViYjM3NGIzMWViZTU2OGY3MGViMyJ9'}, {'domain': '.cashbackbase.com', 'expiry': 1599363180, 'httpOnly': False, 'name': '_gat_gtag_UA_119767146_1', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.cashbackbase.com', 'expiry': 1599449559, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.731395315.1599363120'}, {'domain': 'www.cashbackbase.com', 'httpOnly': False, 'name': 'current-page', 'path': '/', 'secure': False, 'value': 'https%3A%2F%2Fwww.cashbackbase.com%2Fseller-central'}, {'domain': '.cashbackbase.com', 'httpOnly': True, 'name': 'cashbackbasev6_session', 'path': '/', 'secure': False, 'value': 'eyJpdiI6IlNveW42QlNCN29ndXdicE96RVVRTFE9PSIsInZhbHVlIjoidWQ0MmtvS2c5RUg4SVN4YlY4NzNjN2h2Wjl0MGFaOW5CK0FFbU5YOFBoMmJHYlZPQzdmUDFDWEtkU2xEaFppQyIsIm1hYyI6ImM3YTI4YWEyNzEzYTI2ZWIyZTMyOWU5YTc5MzNhMWI5ZTViNGZiZDgzZGYyNmJjNmUxYTUzY2MzZmIzNmUzYmQifQ%3D%3D'}, {'domain': '.cashbackbase.com', 'expiry': 1662435159, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.606942347.1599363120'}]
    for cookie in cookies:
        driver.add_cookie(cookie_dict=cookie)
    driver.get("https://www.cashbackbase.com/seller/order?key=amz_order_id&value=&status=refunded&page=10")
    try:
        WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.ID,'msg-notify')))
        driver.find_element_by_xpath('//*[@id="msg-notify"]//button[@class="close"]').click()
    except:
        pass
    sleep(0.5)
    country = driver.find_element_by_xpath('//*[@id="navbar"]/ul[1]/li[9]/div/a/img').get_attribute('title')
    if country == "UK":
        driver.find_element_by_xpath('//*[@id="navbar"]/ul[1]/li[9]/div/a').click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="navbar"]/ul[1]/li[9]/div/ul')))
        driver.find_element_by_xpath('//*[@id="navbar"]/ul[1]/li[9]/div/ul/li[1]').click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//img[@title="US"]')))
    last_class = driver.find_element_by_xpath('//ul[@class="pagination"]/li[last()]').get_attribute('class')
    while True:
        trs = driver.find_elements_by_xpath('//tbody/tr')
        for tr in trs:
            try:
                order_id = tr.find_element_by_xpath('./td').text
                asin = tr.find_element_by_xpath('.//strong').text
                url = tr.find_element_by_xpath('./td[last()]/p/a').get_attribute('href')
                js = 'window.open("' + url + '")'
                driver.execute_script(js)
                driver.switch_to.window(driver.window_handles[1])
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'line-1')))
                paypal = driver.find_element_by_class_name('line-1').text.replace("PayPal Account:","").strip()
                customer_name = driver.find_element_by_xpath('//div[@class="deal-info-title"]/span').text
                try:
                    profile = driver.find_element_by_xpath('//div[@class="deal-info-title"]//a').get_attribute('href')
                except:
                    profile = ""
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                mp = MysqlPool()
                sql = "insert into tb_cbb_customer(order_id,asin,customer_name,paypal,profile,add_time) values(%s,%s,%s,%s,%s,now())"
                param = [order_id,asin,customer_name,paypal,profile]
                try:
                    mp.insert(sql,param)
                    print("%s入库成功"%order_id)
                except:
                    print("%s已存在"%order_id)
                sleep(0.5)
            except:
                traceback.print_exc()
                print("-----采集出错-----")
        if not last_class:
            driver.find_element_by_xpath('//ul[@class="pagination"]/li[last()]/a').click()
            sleep(1)
        else:break
    driver.quit()


def getTrData(driver):
    trs = driver.find_elements_by_tag_name('tr')
    for tr in trs:
        order_id = tr.find_element_by_xpath('./td').text
        asin = tr.find_element_by_xpath('./strong').text
        print(order_id,asin)
    driver.quit()




if __name__ == "__main__":
    getData()