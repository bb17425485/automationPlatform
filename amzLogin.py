# -*- codeing = utf-8 -*-
# @Time : 2020/9/15 23:10
# @Author : Cj
# @File : amzLogin.py
# @Software : PyCharm


import threading, time
from facebook import FaceBookOperat
from selenium import webdriver
from time import sleep
import configparser,random,threading,traceback
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import win32api,win32con

if __name__ == '__main__':
    config = configparser.RawConfigParser()
    config.read("amz-account.ini", encoding="utf-8")
    nums = 6656
    for i,account in enumerate(config):
        if i > 0:
            print(account)
            options = webdriver.ChromeOptions()
            options.add_argument("user-agent="+str(config[account]['ua']))
            options.add_argument("--start-maximized")
            # options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
            driver.get("https://www.baidu.com/")
            sleep(1)
            for cookie in eval(config[account]['cookies']):
                driver.add_cookie(cookie_dict=cookie)
            # keyword = "cigarette holder"
            # driver.get("https://www.amazon.com/s?k="+keyword+"&ref=nb_sb_noss&page=2")
            # WebDriverWait(driver,15).until(EC.visibility_of_element_located((By.XPATH,'//div[@data-index="0"]')))
            # divs = driver.find_elements_by_xpath('//div[@data-index="0"]/../div')
            # for div in divs:
            #     asin = div.get_attribute("data-asin")
            #     print("-----已留言数量：",nums,"-----")
            #     if asin and asin not in ["B083SH3BP3","B0811855ZX","B08BLNSGHK","B06XPLMFDF","B0897KZF9Z","B07W7R8G7S","B01AMRK4S8","B07PZJX96K","B07F3FN2GX"]:
            #         print(asin)
            #         review_url = "https://www.amazon.com/product-reviews/"+asin+"?ie=UTF8&reviewerType=all_reviews"
            #         js = 'window.open("'+review_url+'")'
            #         driver.execute_script(js)
            #         driver.switch_to.window(driver.window_handles[1])
            #         try:
            #             while True:
            #                 WebDriverWait(driver, 10).until(
            #                     EC.visibility_of_element_located((By.ID, 'cm_cr-review_list')))
            #                 review_div_list = driver.find_elements_by_xpath(
            #                     '//div[@data-a-expander-name="review_comment_expander"]')
            #                 for review_div in review_div_list:
            #                     review_div.find_element_by_xpath('./a').click()
            #                     sleep(0.5)
            #                     try:
            #                         WebDriverWait(review_div, 3).until(
            #                             EC.visibility_of_element_located(
            #                                 (By.XPATH, './/textarea[contains(@placeholder,"Respond to this review")]')))
            #                     except TimeoutException:
            #                         WebDriverWait(review_div, 5).until(
            #                             EC.visibility_of_element_located(
            #                                 (By.XPATH, './/span[contains(text(),"Comment")]')))
            #                         review_div.find_element_by_xpath('.//span[contains(text(),"Comment")]/..').click()
            #                         WebDriverWait(review_div, 5).until(
            #                             EC.visibility_of_element_located(
            #                                 (By.XPATH, './/textarea[contains(@placeholder,"Respond to this review")]')))
            #                     review_div.find_element_by_xpath(
            #                         './/textarea[contains(@placeholder,"Respond to this review")]').send_keys(
            #                         "Thank you for purchasing our product, we now have a free product to test, you can contact my email: g1150082245@gmail。com")#
            #                     review_div.find_element_by_xpath('.//span[text()="Post a comment"]/../..').click()
            #                     sleep(0.5)
            #                     review_div.find_element_by_xpath('./a').click()
            #                     nums += 1
            #                     sleep(1)
            #                 try:
            #                     WebDriverWait(driver, 5).until(
            #                         EC.visibility_of_element_located(
            #                             (By.XPATH, './/li[@class="a-last"]')))
            #                     driver.find_element_by_class_name('a-last').click()
            #                     sleep(1.5)
            #                 except TimeoutException as e:
            #                     print("已到最后一页")
            #                     break
            #         except:
            #             traceback.print_exc()
            #         driver.close()
            #         driver.switch_to.window(driver.window_handles[0])

            driver.get("https://www.amazon.com")
            sleep(1)
            driver.find_element_by_xpath('//*[@id="nav-orders"]').click()
            WebDriverWait(driver,15).until(EC.visibility_of_element_located((By.ID,'ap_password')))
            driver.find_element_by_id('ap_password').send_keys(config[account]['pwd'])
            sleep(1)
            driver.find_element_by_id('signInSubmit').click()
            sleep(3)
            cookies = driver.get_cookies()
            driver.quit()
            # config.set(account, "cookies", cookies)
            # config.write(open("amz-account.ini", "w"))
            # driver.quit()
            # while True:
            #     sleep(5)
            #     print(driver.get_cookies())
            # sleep(5000)
            # driver.quit()
    # cookies = [{'domain': 'www.amazon.com', 'expiry': 1601631120, 'httpOnly': False, 'name': 'csm-hit', 'path': '/', 'secure': False, 'value': 's-Q9M3RCV1QPEGHPBT8BQ9|1601026320358'}, {'domain': '.amazon.com', 'expiry': 1632562320, 'httpOnly': False, 'name': 'lc-main', 'path': '/', 'secure': False, 'value': 'en_US'}, {'domain': '.amazon.com', 'expiry': 1632562319, 'httpOnly': True, 'name': 'sst-main', 'path': '/', 'secure': True, 'value': 'Sst1|PQHOBMcaMELNVPgZHwpIh-yVCXwtcpypLNHu93W5m3a5tshZy52LF_Vk1V4oo-7oE8Snqyl-QqfbSKfYe5oozWa5Xc5s4c_Ou_8G3rV1940Vd39D-TgMlPSHC1e_V3cUTbQ68-HVmmVkmW2aK2P5W3sEvk61fLRtG_DCW--TcWmMKX2s9WfQ2kY_L6X5_QMCSWl6M4kv25JBYMLvV_j4DZ7hhFMKolXQC1fI7LG_Na2dZuQZtNADuPx7GfxgkPT_kN9d1qT7O3HZWHjf_XjvCAuwMyfscZTJt2VcLurt43ofonI'}, {'domain': '.amazon.com', 'expiry': 1632562320, 'httpOnly': False, 'name': 'i18n-prefs', 'path': '/', 'secure': False, 'value': 'USD'}, {'domain': '.amazon.com', 'expiry': 1632562319, 'httpOnly': True, 'name': 'sess-at-main', 'path': '/', 'secure': True, 'value': '"8TblotlRIZCz/mRL44ZAN9l/7zOYXH+Baxga8k0Frwo="'}, {'domain': '.amazon.com', 'httpOnly': False, 'name': 'skin', 'path': '/', 'secure': False, 'value': 'noskin'}, {'domain': '.amazon.com', 'expiry': 1632562319, 'httpOnly': True, 'name': 'at-main', 'path': '/', 'secure': True, 'value': 'Atza|IwEBIKfY8NBe7o15T11yJDhbVgIjJeENbe6BhwFwyHyOoU97-N6nzEWKif1NI9dTBuOoqhlGVl9Og88yjaehIXfpO3AUqPwUteKO1eO4auPsNSQtbJaRJrjWf_9WAkvE1wvMzo-vQjnIbvi6kzYTENeRcVgju_n0iVQgRk6aPZ9t-UmtjsM-SV-3fNnNig8dhyJnFTFtVdgEGoII0XIPUpkzbMbA'}, {'domain': '.amazon.com', 'expiry': 1632562321, 'httpOnly': False, 'name': 'ubid-main', 'path': '/', 'secure': True, 'value': '132-5303979-3406626'}, {'domain': '.amazon.com', 'expiry': 1632562320, 'httpOnly': False, 'name': 'x-main', 'path': '/', 'secure': False, 'value': '"qLeEoETn6dtn@OcPWhAH5AxquOleaY0ezF937udQFB5yb1W8EawoLKpUHB8Oo7li"'}, {'domain': '.amazon.com', 'expiry': 1632562321, 'httpOnly': False, 'name': 'session-id', 'path': '/', 'secure': True, 'value': '132-3226474-9551338'}, {'domain': '.amazon.com', 'expiry': 1632562320, 'httpOnly': False, 'name': 'session-token', 'path': '/', 'secure': False, 'value': '"rzw88peCfNxGdgHlcJ9KjnQWRsz1Qg4UJoh/In+JeZUIQx7lMaGuZSpfMsd+RvyuJ5hVNgjsKhvHdMazuuyRh2gP5e+b8QX6WtLwIy5fp7EzUzDcszIHqQIekh426ImUAA8wx7U62scJ77xZohxgXObuPnRtLHdPXtBUsGR5I+FPK3zj0NKf7DO+qTHw+kEFIAIknj2s1OQFPBuBNKk4v9eRHPhiiIW0x6wo/OHd1fc="'}, {'domain': '.amazon.com', 'expiry': 1632562321, 'httpOnly': False, 'name': 'session-id-time', 'path': '/', 'secure': False, 'value': '2082787201l'}]



        # print(str(driver.get_cookies()).replace("\'","\"").replace("\"\"","\"").replace("False","false").replace("True","true"))





