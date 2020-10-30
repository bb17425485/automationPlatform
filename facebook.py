# -*- codeing = utf-8 -*-
# @Time : 2020/9/10 17:15
# @Author : Cj
# @File : fb.py
# @Software : PyCharm

from selenium import webdriver
from time import sleep
from datetime import datetime,timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import configparser
from db import MysqlPool

class FaceBookOperat:

    def __init__(self,group_id,keyword,content,nums,post_id):
        self.group_id = group_id
        self.keyword = keyword
        self.content = content
        self.nums = nums
        self.post_id = post_id

    def startWork(self):
        print("--目标群组:%s,搜索词:%s,任务数:%s--"%(self.group_id,self.keyword,str(self.nums)))
        config = configparser.RawConfigParser()
        config.read("fb-user.ini", encoding="utf-8")
        done_nums = 0
        for i, account in enumerate(config):
            print("*****已完成数量%s*****"%str(done_nums))
            if done_nums == int(self.nums):
                print("*****%s的任务已全部完成*****"%self.group_id)
                break
            if i > 0:
                acc = {}
                pwd = config[account]['pwd']
                ua = config[account]['user-agent']
                try:
                    cookies = config[account]['cookies']
                    if len(cookies) == 0:
                        cookies = self.login(account, pwd, ua)
                except KeyError:
                    cookies = self.login(account,pwd,ua)
                if cookies is None:continue
                acc['account'] = account
                acc['cookies'] = cookies
                acc['ua'] = ua
                try:
                    last_time_str = config[account][self.group_id]
                    last_time = datetime.strptime(last_time_str,"%Y-%m-%d %H:%M:%S")
                    compare_time = last_time + timedelta(days=1)
                    if datetime.now() < compare_time:
                        print("---帐号%s于%s已在%s发布评论---"%(account,last_time_str,self.group_id))
                        continue
                except KeyError:
                    pass
                except ValueError:
                    pass
                num = self.doComment(acc)
                done_nums += num

    @staticmethod
    def login(account, pwd, ua):
        print("~~~~~%s开始自动登录并保存cookies信息~~~~~"%account)
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent="+ua)
        options.add_argument("--start-maximized")
        # options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.facebook.com/")
        sleep(1)
        driver.find_element_by_name("email").send_keys(account)
        driver.find_element_by_name("pass").send_keys(pwd)
        driver.find_element_by_name("pass").send_keys(Keys.ENTER)
        sleep(1)
        if driver.current_url == "https://www.facebook.com/?sk=welcome":
            print("~~~~~登录成功~~~~~")
            cookies = driver.get_cookies()
            config = configparser.RawConfigParser()
            config.read("fb-user.ini", encoding="utf-8")
            config.set(account, "cookies", driver.get_cookies())
            config.write(open("fb-user.ini", "w"))
            driver.quit()
            return cookies
        else:
            print("~~~~~登录失败~~~~~")
            driver.quit()
            return None

    def doComment(self,acc):
        print("*****帐号",acc['account'],"开始执行*****")
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent="+acc['ua'])
        options.add_argument("--start-maximized")
        # options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        try:
            driver.get("https://www.facebook.com/")
            if type('') is type(acc['cookies']):
                cookie_list = eval(acc['cookies'])
            else:
                cookie_list = acc['cookies']
            for cookie in cookie_list:
                driver.add_cookie(cookie_dict=cookie)
            # driver.get("https://www.facebook.com/groups/"+self.group_id+"/")
            # driver.get("https://www.facebook.com/search/groups/?q=Coupons, Codes, Glitches & Deals Under")
            driver.get("https://www.facebook.com/search/groups/?q=%s"%self.group_id)
            # driver.get("https://www.facebook.com/search/groups/?q=Super Savings(Codes,Deals,Coupons 10-99 off)&epa=SEARCH_BOX")
            # driver.find_element_by_name("q").send_keys("Super Savings(Codes,Deals,Coupons 10-99 off)")
            sleep(1)
            try:
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      '//div[@id="BrowseResultsContainer"]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/button')))
                group_status = driver.find_element_by_xpath(
                    '//div[@id="BrowseResultsContainer"]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/button').text
            except:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          '//div[@id="BrowseResultsContainer"]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/a')))
                    group_status = driver.find_element_by_xpath(
                        '//div[@id="BrowseResultsContainer"]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/a').text
                except:
                    print("-----查找群组%s出错-----"%self.group_id)
                    driver.quit()
                    return 0
            print("*****status:",group_status,"*****")
            if group_status == "请求已发送":
                print("-----%s加入群组请求已发送-----"%acc['account'])
                driver.quit()
                return 0
            elif group_status == "加入":
                driver.find_element_by_xpath('//div[@id="BrowseResultsContainer"]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/a').click()
                WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      '//div[contains(@aria-label,"回答问题")]')))
                bo = self.answerQuersion(driver)
                if bo:
                    print("-----回答问题成功-----")
                else:
                    print("-----回答问题失败-----")
                driver.quit()
                return 0
            elif group_status == "已加入":
                try:
                    driver.find_element_by_xpath('//*[@id="BrowseResultsContainer"]/div[1]//a').click()
                    WebDriverWait(driver, 15).until(
                        EC.visibility_of_element_located((By.NAME, 'query')))
                    driver.find_element_by_name("query").send_keys(self.keyword)  # PQSTISPT 50CQ5GQI
                    driver.find_element_by_xpath('//span[@class="uiSearchInput"]/span/button').click()
                    WebDriverWait(driver, 15).until(
                        EC.visibility_of_element_located((By.XPATH, '//div[@id="BrowseResultsContainer"]')))
                    driver.find_element_by_xpath(
                        '//*[@id="BrowseResultsContainer"]/div/div/div/div/div/div/div/div/div[3]/div/div/div[3]//a').click()
                    print("*****点赞成功*****")
                    WebDriverWait(driver, 15).until(
                        EC.visibility_of_element_located((By.XPATH, '//div[contains(@aria-label,"写评论...")]')))
                    driver.find_element_by_xpath('//form[@class="commentable_item"]/div/div[2]/div[2]//a').click()
                    sleep(1)
                    driver.find_element_by_xpath('//div[contains(@aria-label,"写评论...")]').send_keys(self.content)
                    sleep(1)
                    driver.find_element_by_xpath('//div[contains(@aria-label,"写评论...")]').send_keys(Keys.ENTER)
                    sleep(1)
                    print("*****评论成功*****")
                    try:
                        driver.find_element_by_xpath('//a[@title="发送给好友或发布到你的时间线上。"]').click()
                        WebDriverWait(driver, 15).until(
                            EC.visibility_of_element_located((By.XPATH, '//ul[@role="menu"]')))
                        driver.find_element_by_xpath('//ul[@role="menu"]/li').click()
                    except Exception as e:
                        print(e)
                    sleep(1)
                    print("*****分享成功*****")
                    mp = MysqlPool()
                    sql = "update tb_post set status=%s,finish_time=%s where id=%s"
                    param = ["finish",datetime.now(),str(self.post_id)]
                    mp.update(sql,param)
                    print("*****更新数据库成功*****")
                    config = configparser.RawConfigParser()
                    config.read("fb-user.ini", encoding="utf-8")
                    config.set(acc['account'], self.group_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    config.set(acc['account'], "cookies", driver.get_cookies())
                    config.write(open("fb-user.ini", "w"))
                    sleep(1)
                    print("*****更新帐号配置文件成功*****")
                    print("*****帐号", acc['account'], "执行完成*****")
                    return 1
                except TimeoutException as e:
                    print(e)
                    return 0
        except Exception as e:
            print(e)
            print("-----%s任务出错-----"%acc['account'])
            return 0
        finally:
            driver.quit()


    def answerQuersion(self, driver):
        print("-----开始回答问题-----")
        try:
            if self.group_id == "Super Savings(Codes,Deals,Coupons 10-99 off)":
                driver.find_element_by_xpath(
                    '//*[@id="fb"]/body/div[15]/div[2]/div/div/div/div/div/div/div[2]/div/div[3]//input').click()
                sleep(1)
                driver.find_element_by_xpath(
                    '//*[@id="fb"]/body/div[15]/div[2]/div/div/div/div/div/div/div[2]/div/div[4]//input').click()
                sleep(1)
                driver.find_element_by_xpath(
                    '//*[@id="fb"]/body/div[15]/div[2]/div/div/div/div/div/div/div[2]/div/div[5]//input').click()
                sleep(1)
                driver.find_element_by_xpath('//div[@role="dialog"][last()]/div[3]/span[2]').click()
                return True
            else: return False
        except:
            return False