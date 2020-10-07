# -*- codeing = utf-8 -*-
# @Time : 2020/9/25 16:55
# @Author : Cj
# @File : zzz.py
# @Software : PyCharm

from db import MysqlPool
import random,string,configparser,re,json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from time import sleep
from datetime import datetime
from fake_useragent import UserAgent
from multiprocessing import Pool,Process
import fileinput,os

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

def filter_emoji(desstr, restr=''):
    # 过滤表情
    res = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
    return res.sub(restr, desstr)

def filter_str(desstr, restr=''):
    # 过滤除中英文及数字及英文标点以外的其他字符
    res = re.compile("[^\u4e00-\u9fa5^. !//_,$&%^*()<>+\"'?@#-|:~{}+|—^a-z^A-Z^0-9]")
    return res.sub(restr, desstr)

def abc(a,b,c):
    print("123")
    sleep(c)
    print(a+b)
    return True,a+b

def div_list(ls,n):
	if not isinstance(ls,list) or not isinstance(n,int):
		return []
	ls_len = len(ls)
	if n<=0 or 0==ls_len:
		return []
	if n > ls_len:
		return []
	elif n == ls_len:
		return [[i] for i in ls]
	else:
		j = ls_len/n
		k = ls_len%n
		### j,j,j,...(前面有n-1个j),j+k
		#步长j,次数n-1
		ls_return = []
		for i in range(0,(n-1)*j,j):
			ls_return.append(ls[i:i+j])
		#算上末尾的j+k
		ls_return.append(ls[(n-1)*j:])
		return ls_return


def bisector_list(tabulation: list, num: int):
    """
    将列表平均分成几份
    :param tabulation: 列表
    :param num: 份数
    :return: 返回一个新的列表
    """
    new_list = []

    '''列表长度大于等于份数'''
    if len(tabulation) >= num:
        '''remainder:列表长度除以份数，取余'''
        remainder = len(tabulation) % num
        if remainder == 0:
            '''merchant:列表长度除以分数'''
            merchant = int(len(tabulation) / num)
            '''将列表平均拆分'''
            for i in range(1, num + 1):
                if i == 1:
                    new_list.append(tabulation[:merchant])
                else:
                    new_list.append(tabulation[(i - 1) * merchant:i * merchant])
            return new_list
        else:
            '''merchant：列表长度除以分数 取商'''
            merchant = int(len(tabulation) // num)
            '''remainder:列表长度除以份数，取余'''
            remainder = int(len(tabulation) % num)
            '''将列表平均拆分'''
            for i in range(1, num + 1):
                if i == 1:
                    new_list.append(tabulation[:merchant])
                else:
                    new_list.append(tabulation[(i - 1) * merchant:i * merchant])
                    '''将剩余数据的添加前面列表中'''
                    if int(len(tabulation) - i * merchant) <= merchant:
                        for j in tabulation[-remainder:]:
                            new_list[tabulation[-remainder:].index(j)].append(j)
            return new_list
    else:
        '''如果列表长度小于份数'''
        for i in range(1, len(tabulation) + 1):
            tabulation_subset = [tabulation[i - 1]]
            new_list.append(tabulation_subset)
        return new_list

def removeTxtLine(txt,index):
    with open(txt) as fp_in:
        with open('temp.txt', 'w') as fp_out:
            fp_out.writelines(line for i, line in enumerate(fp_in) if i != index)
    os.rename(txt, 'test.bak')
    os.rename('temp.txt', txt)
    os.remove('test.bak')

if __name__ == '__main__':
    removeTxtLine('keyword_bak.txt',0)


    # for line in fileinput.input("keyword_bak.txt", inplace=1):
    #     if not fileinput.isfirstline():
    #         print(line.replace('\n', ''))

    # a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # for i in range(3):
    #     print(i,a[0])
    #     a.pop(0)
    #     sleep(1)
    # print(a)
    # numList = []
    # param = [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4], [5, 5, 5]]
    # for i in range(5):
    #     p = Process(target=abc,args=param[i])
    #     numList.append(p)
    #     p.start()  # 用start()方法启动进程，执行do()方法
    # for proc in numList:
    #     proc.join()
    # print("------------")

    # x = bisector_list(a, 4)
    # print(x)
    # pool = Pool(5)
    # param = [[1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5]]
    # res = pool.starmap(abc,param)
    # pool.close()
    # pool.join()
    # for rrr in res:
    #     print(rrr[1])
    # print(div_list([3,4,5,6,7,8,9,10,11,12,13,14,15],3))












    # b = "aaaa"
    # c = "bbbbbbbbbbbb"
    # a = 'https://www.facebook.com/groups/436275050546458/?ref=br_rs%s'%b+c
    # b = "💥💥💥Promotions, Great Deals& Coupons💥💥💥"
    # r3 = "[.!//_,$&%^*()<>+\"'?@#-|:~{}]+|[——！\\\\，。=？、：“”‘'《》【】￥……（）]+"
    # a = ["a","b"]
    # for i,v in enumerate(a):
    #     print(i)
    # p = re.compile("\?.*")
    # print(re.sub(r3, "",b))
    # print(filter_str(b))
    # d = 'October 17, 2018'
    # print(datetime.strptime(d, '%B %d, %Y').strftime("%Y-%m-%d"))
    # a = b'{"code":0,"success":"true","msg":"","data":[{"IP":"114.99.22.88","Port":32610},{"IP":"223.241.168.45","Port":38407},{"IP":"59.41.131.6","Port":41130},{"IP":"183.161.1.164","Port":40511},{"IP":"183.32.143.254","Port":29351},{"IP":"117.66.140.133","Port":27527},{"IP":"27.42.183.122","Port":34062},{"IP":"175.4.184.25","Port":32100},{"IP":"114.107.148.248","Port":36539},{"IP":"183.165.244.74","Port":38761},{"IP":"124.113.242.253","Port":29971},{"IP":"106.44.36.186","Port":42776},{"IP":"163.179.206.202","Port":32904},{"IP":"110.18.2.96","Port":32799},{"IP":"121.57.165.178","Port":34905},{"IP":"59.60.120.251","Port":37361},{"IP":"183.1.192.157","Port":26628},{"IP":"123.171.45.121","Port":49117},{"IP":"220.175.251.120","Port":23247},{"IP":"113.76.59.181","Port":48612},{"IP":"218.64.154.213","Port":26922},{"IP":"58.255.7.249","Port":46348},{"IP":"121.233.206.91","Port":29619},{"IP":"117.66.140.98","Port":47882},{"IP":"36.6.138.53","Port":31536},{"IP":"125.106.86.147","Port":32910},{"IP":"183.164.246.198","Port":35804},{"IP":"123.128.94.39","Port":35860},{"IP":"114.97.215.2","Port":31757}]}'
    # b = json.loads(a)
    # for li in list(b['data']):
    #     print(li)
    # res = re.compile("\y.*")
    # c = res.sub(a, "")
    # c = re.sub("\(.*", "", a)
    # d = re.findall("\d",c)
    # x = ""
    # for dd in d:
    #     x += dd
    # print(x)








    # c = DownThread()
    # t = threading.Thread(target=c.run, args=(10,))
    # t.start()
    # time.sleep(3)
    # c.terminate()
    # t.join()
    # t.is_alive()






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
