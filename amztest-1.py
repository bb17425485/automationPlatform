# -*- codeing = utf-8 -*-
# @Time : 2020/10/17 15:50
# @Author : Cj
# @File : fbtest-1.py
# @Software : PyCharm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from logger import Logger
import re,multiprocessing,random,configparser
from fake_useragent import UserAgent

all_log = Logger('log/amz_account_all.log', level='debug')

def doWork(url):
    # config = configparser.RawConfigParser()
    # config.read("amz-ca-account.ini", encoding="utf-8")
    options = Options()
    ua = UserAgent().chrome
    ua = re.sub("Chrome/\d{2}", "Chrome/"+str(random.randint(49,85)) , ua)
    # ua = 'Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.1453.116 Safari/537.36'
    # print(ua)
    # ua = config['no1']['ua']
    options.add_argument("user-agent=" + ua)
    # options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("log-level=3")
    # options.add_argument('blink-settings=imagesEnabled=false')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(400,300)
    cookies = [{"domain":".amazon.com","expirationDate":2233745699.655778,"hostOnly":False,"httpOnly":False,"name":"ubid-main","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"132-8813534-9194430"},{"domain":".amazon.com","expirationDate":2082787201.390767,"hostOnly":False,"httpOnly":False,"name":"session-token","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"\"6jioo9dKDjAUqksAEUOs8tkH8mryj87pnjTepRGzIWeZnAo/uFp86SfrZpUohMh3OVTbMBHjxY6hi6lQ5/BX7WfU96DtUsRNDgYIZ3wg9L8TNa7sWYrrvlOLbyIVrkyXQ1YIIbUdZuIPxYcS2jQbM7zIaKC9sxwDEbf/O/eMnerX78JI0zLUvezw5qmkRygjStZpRi9nBe4z7LVLhPZ9kA==\""},{"domain":".amazon.com","expirationDate":1634461817.464778,"hostOnly":False,"httpOnly":False,"name":"i18n-prefs","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"USD"},{"domain":".amazon.com","expirationDate":1634461817.464754,"hostOnly":False,"httpOnly":False,"name":"x-main","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"\"VRbmyyTVH@lveo2DxwcmgrjIvVrm7qyzrE2RdThu0TZ2Nnt8f9uIO8qepf9pmrE4\""},{"domain":"www.amazon.com","expirationDate":1633265690,"hostOnly":True,"httpOnly":False,"name":"csm-hit","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"tb:s-9NBGTA402WKBAPFBYTXR|1603025689798&t:1603025690575&adb:adblk_no"},{"domain":".www.amazon.com","expirationDate":1608197420,"hostOnly":False,"httpOnly":False,"name":"csd-key","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"eyJ2IjoxLCJraWQiOiI4ZmNjYzIiLCJrZXkiOiJOclh4Vk9NNlFJNWhYNUU0Vk5LQUlDM0wzUjdUNkNHRjRmRDRqN3AwYkwwOWdvU1lvTWFEeWVmZEx6cVUreDVZZTJHWkVMVjBPZHFtLzlSWXlBanlBYmVsTXR2cmdUMkFLemswazdseU1xMWtjeG1YbFViWER6UHkzM1FZUHYzaHhKWmtDQWMvemVPS0VEdUNYdWhWNEZDM1pSemZ3UGdta0h4d2l1SW11Q05DL3lnNk03RC9hekFOVlhNblNVbVd0ZExjUktFNHRTQjczcnZseFRrUlRFVVVNMGp5cjN6M1NydzZGcjJTV0luYmREaVg0K0ppVzhGcGhUOWJldFlmWWNUMEp3T0V5UWRyc01CamxiRFhUVFFkNlRWU05GRkJDb2FHaTBBSVlqcGZUQW9FU0dOMlk4cGI2ZHJPQmswcUpEK2FUcWpLaS80amo1QWhJTXl3WEE9PSJ9"},{"domain":".amazon.com","expirationDate":1634524031.678436,"hostOnly":False,"httpOnly":True,"name":"sp-cdn","path":"/","sameSite":"unspecified","secure":True,"session":False,"storeId":None,"value":"\"L5Z9:CN\""},{"domain":".amazon.com","expirationDate":2233745699.65589,"hostOnly":False,"httpOnly":False,"name":"session-id-time","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"2082787201l"},{"domain":".amazon.com","expirationDate":1634461815.227964,"hostOnly":False,"httpOnly":True,"name":"at-main","path":"/","sameSite":"unspecified","secure":True,"session":False,"storeId":None,"value":"Atza|IwEBIIByFl3fO_epDc_IgeQmFoX01aOVdjk5pO0DjqFO588DFCgjQUrnfrFY4nj1xZrVhpwshh2PCPTvDb0YXgVqZueKhJHdQ4UJiblJE1x4VR2RmOsuSbq7jbLy5dh_-YvwZhX31TP65hf7XLzAU6cmwp-x-zBIynm4Wne7rzu6G3EH4JYE37ZIvbKsJ24HTS-LIbzhkkuJUFl6JUfNF1pIYAwa"},{"domain":".amazon.com","expirationDate":1697212874,"hostOnly":False,"httpOnly":False,"name":"s_dslv","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"1602604874334"},{"domain":".amazon.com","expirationDate":2016336910,"hostOnly":False,"httpOnly":False,"name":"s_vnum","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"2016336910355%26vn%3D5"},{"domain":".amazon.com","expirationDate":1634461817.4648,"hostOnly":False,"httpOnly":False,"name":"lc-main","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"en_US"},{"domain":".amazon.com","expirationDate":2034604874,"hostOnly":False,"httpOnly":False,"name":"s_nr","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"1602604874325-Repeat"},{"domain":".amazon.com","expirationDate":1743088530,"hostOnly":False,"httpOnly":False,"name":"s_pers","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"%20s_fid%3D0E27D31BD56383E9-3CFD0121F9F53866%7C1743088530834%3B%20s_dl%3D1%7C1585323930836%3B%20gpv_page%3DUS%253ASD%253ASOA-home%7C1585323930844%3B%20s_ev15%3D%255B%255B%2527www.baidu.com%2527%252C%25271584108648930%2527%255D%252C%255B%2527SCSOAStriplogin%2527%252C%25271584108685311%2527%255D%252C%255B%2527SCHelpUSSOA-header%2527%252C%25271585322130850%2527%255D%255D%7C1743088530850%3B"},{"domain":".amazon.com","expirationDate":1634461815.228004,"hostOnly":False,"httpOnly":True,"name":"sess-at-main","path":"/","sameSite":"unspecified","secure":True,"session":False,"storeId":None,"value":"\"j58QvyLE4MrctxHR5TJl9z5ybqDxs1lLaviUqqlBo+c=\""},{"domain":".amazon.com","expirationDate":2233745699.65595,"hostOnly":False,"httpOnly":False,"name":"session-id","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"130-2343992-9258319"},{"domain":".amazon.com","hostOnly":False,"httpOnly":False,"name":"skin","path":"/","sameSite":"unspecified","secure":False,"session":True,"storeId":None,"value":"noskin"},{"domain":".amazon.com","expirationDate":1634461815.228034,"hostOnly":False,"httpOnly":True,"name":"sst-main","path":"/","sameSite":"unspecified","secure":True,"session":False,"storeId":None,"value":"Sst1|PQGmODmmRVTr4wTLLX7mC_VMCe0J3P52_mD3AvlkxGjwTeD5t2uFDgSPioYSnBPz5FAKe4eEMCynHWDP9mbjfHWeq27W_XPxCj7PjidcMlr7TLPMy0pnr6s_mUeQvv8G8ODlmUTJetjg2a8lcjR-x5paCvCJByvRtwGT37gKFa-ayxKUJsZbAv09O-TDHtkNVYqU3QxSvirmTT0eZCb2tzS63lFWSxGyP6BmOZP8NymMfpMUqe9XOMMgR02jZ_WwUy0ZYxmDo3MoC-Ygd_ernXnlFasORJS71q6HnPlois37w1Q"},{"domain":".amazon.com","expirationDate":2082787202.245597,"hostOnly":False,"httpOnly":False,"name":"ubid-acbus","path":"/","sameSite":"unspecified","secure":False,"session":False,"storeId":None,"value":"135-5461869-9698219"}]
    # cookies = config['no1']['cookies']
    driver.get("https://www.baidu.com")
    for cookie in cookies:
        cookie.pop('sameSite')
        driver.add_cookie(cookie_dict=cookie)
    driver.get(url)

    # driver.find_element_by_xpath('//li[@role="presentation"][2]').click()
    # sleep(3)
    # driver.find_element_by_xpath('//li[text()="Product details"]').click()
    # sleep(3)
    # driver.find_element_by_xpath('//textarea').send_keys("Does this product have 2 inches")
    # sleep(2)
    # driver.find_element_by_xpath('//span[text()="Send Message"]').click()
    sleep(1000)
    # while True:
    #     sleep(5)
    #     print(driver.get_cookies())

if __name__ == "__main__":
    a = 'https://www.amazon.com/askseller?marketplaceID=ATVPDKIKX0DER&sellerID=A1XTOMSTOXPAYA&_encoding=UTF8&ref_=v_sp_contact_seller&'
    b = 'https://www.amazon.com/askseller?marketplaceID=ATVPDKIKX0DER&sellerID=A3G27BQJYXZZ9M&_encoding=UTF8&ref_=v_sp_contact_seller&'
    c = 'https://www.amazon.com/askseller?marketplaceID=ATVPDKIKX0DER&sellerID=A2DAVTN86TOFBR&_encoding=UTF8&ref_=v_sp_contact_seller&'
    url_list = [a,b,c,a,b,c,a,b,c,a]
    process_list = []
    for url in url_list:
        sleep(1)
        process = multiprocessing.Process(target=doWork, args=(url,))
        process.start()
        process_list.append(process)
    for p in process_list:
        p.join()
    print("执行结束")
    # c = "https://www.amazon.com"
    # doWork(a)

