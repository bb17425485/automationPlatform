# -*- codeing = utf-8 -*-
# @Time : 2020/9/22 9:55
# @Author : Cj
# @File : fbJob.py
# @Software : PyCharm

from db import MysqlPool
import configparser,random,traceback,re
from selenium import webdriver
from time import sleep
from datetime import datetime,timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from logger import Logger

all_log = Logger('log/all.log', level='debug')
error_log = Logger('log/error.log', level='error')
# log.logger.debug('debug')
# log.logger.info('info')
# log.logger.warning('警告')
# log.logger.error('报错')
# log.logger.critical('严重')

def groupTask():
    config = configparser.RawConfigParser()
    config.read("fb-user.ini", encoding="utf-8")
    keywords = ["amazon code","amazon coupons","the deals","super deal"]
    for i, account in enumerate(config):
        if i == 2:
            acc = {}
            ua = config[account]['user-agent']
            cookies = config[account]['cookies']
            acc['account'] = account
            acc['cookies'] = cookies
            acc['user-agent'] = ua
            collectionGroup(acc,keywords)


def collectionGroup(acc,keywrods):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=" + acc['user-agent'])
    prefs = {
        'profile.default_content_setting_values': {
            'notifications': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.baidu.com/")
    if type('') is type(acc['cookies']):
        cookie_list = eval(acc['cookies'])
    else:
        cookie_list = acc['cookies']
    for cookie in cookie_list:
        driver.add_cookie(cookie_dict=cookie)
    for keyword in keywrods:
        # 公开小组 & 非公开小组
        group_types = ["&epa=FILTERS&filters=eyJncm91cHNfc2hvd19vbmx5Ijoie1wibmFtZVwiOlwicHVibGljX2dyb3Vwc1wiLFwiYXJnc1wiOlwiXCJ9In0%3D","&epa=FILTERS&filters=eyJncm91cHNfc2hvd19vbmx5Ijoie1wibmFtZVwiOlwiY2xvc2VkX2dyb3Vwc1wiLFwiYXJnc1wiOlwiXCJ9In0%3D"]
        for group_num,group in enumerate(group_types):
            driver.get("https://www.facebook.com/search/groups/?q=%s"%keyword+group)
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH,'//div[@id="BrowseResultsContainer"]')))
            for i in range(15):
                ActionChains(driver).send_keys(Keys.END).perform()
                sleep(1.5)
                if i > 10:
                    try:
                        WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located((By.ID, 'browse_end_of_results_footer')))
                        break
                    except:
                        pass
            divs = driver.find_elements_by_xpath('//div[@id="BrowseResultsContainer"]/../div')
            for j,div in enumerate(divs):
                if j == 0:
                    proDivs = div.find_elements_by_xpath('./div')
                elif j == 1:
                    proDivs = div.find_elements_by_xpath('./div/div/div')
                else:
                    proDivs = div.find_elements_by_xpath('./div/div')
                if len(proDivs) <= 1:
                    break
                for pro in proDivs:
                    pro_url = pro.find_element_by_tag_name('a').get_attribute("href")
                    if group_num == 0:
                        pro_url = re.sub("\?.*", "members/", pro_url)
                    js = 'window.open("' + pro_url + '")'
                    driver.execute_script(js)
                    driver.switch_to.window(driver.window_handles[1])
                    sleep(1000)
                    try:
                        if group_num == 0:
                            WebDriverWait(driver, 5).until(
                                EC.visibility_of_element_located((By.XPATH, '//div[@id="groupsMemberBrowser"]')))
                        else:
                            WebDriverWait(driver, 5).until(
                                EC.visibility_of_element_located((By.XPATH, '//div[@id="content_container"]')))
                        group_name = driver.find_element_by_xpath('//div[@data-testid="group_sidebar_nav"]//a').text
                        group_admin = ""
                        if group_num == 0:
                            nums = driver.find_element_by_xpath('//div[@id="groupsMemberBrowser"]//span').text.replace(",","")
                            admins_div = driver.find_elements_by_xpath('//div[@data-testid="GroupAdminGrid"]/ul/div')
                            for admin_div in admins_div:
                                group_admin += admin_div.find_element_by_tag_name('img').get_attribute("aria-label") + "|"
                        else:
                            nums = driver.find_element_by_xpath('//div[@id="pagelet_group_about"]/div[2]//span').text.replace("成员 · ","").replace(",","")
                            admins_div = driver.find_elements_by_xpath('//div[@id="pagelet_group_about"]/div[2]/div[2]/div[2]/a')
                            for admin_div in admins_div:
                                group_admin += admin_div.find_element_by_tag_name('img').get_attribute("aria-label") + "|"
                        if int(nums) < 4000:
                            error_log.logger.error("-----%s人数为%s，跳过-----"%(group_name,nums))
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            continue
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        mp = MysqlPool()
                        sql = "insert into tb_group(name,nums,admins,type,url,add_time) values(%s,%s,%s,%s,%s,now())"
                        param = [filter_str(group_name),nums,filter_str(group_admin),group_num,pro_url]
                        try:
                            mp.insert(sql,param)
                            all_log.logger.info("-----%s入库成功-----"% group_name)
                        except:
                            error_log.logger.error("-----%s已入库，跳过-----" % group_name)
                        sleep(1)
                    except:
                        traceback.print_exc()
                        error_log.logger.error("*****获取%s信息出错*****"%pro_url)
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

def getTask():
    mp = MysqlPool()
    sql = "select * from tb_post where state = 'working'"
    task_list = mp.fetch_all(sql,None)
    if task_list:
        content_sql = "select content from tb_comment"
        content_list = mp.fetch_all(content_sql,None)
        num_list = []
        for task in task_list:
            num_list.append(task['id'])
        all_log.logger.info("-----本次执行的任务列表：%s-----"%num_list)
        for task in task_list:
            config = configparser.RawConfigParser()
            config.read("fb-user.ini", encoding="utf-8")
            for i, account in enumerate(config):
                if i > 1:
                    all_log.logger.info("#####等待5秒后，下一个帐号开始执行#####")
                    sleep(5)
                if i > 0:
                    all_log.logger.info("*****帐号%s开始执行*****%s"%(account,task['id']))
                    if account in task['accounts']:
                        all_log.logger.info("*****该账号已执行过此任务，跳过*****")
                        continue
                    acc = {}
                    pwd = config[account]['pwd']
                    try:
                        ua = config[account]['user-agent']
                        if not ua:
                            ua = UserAgent().chrome
                    except:
                        ua = UserAgent().chrome
                    try:
                        cookies = config[account]['cookies']
                        if len(cookies) == 0:
                            cookies = login(account, pwd, ua)
                    except KeyError:
                        cookies = login(account, pwd, ua)
                    if cookies is None:
                        continue
                    acc['account'] = account
                    acc['cookies'] = cookies
                    acc['user-agent'] = ua
                    try:
                        last_time_str = config[account][task['group_id']]
                        last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
                        compare_time = last_time + timedelta(days=1)
                        if datetime.now() < compare_time:
                            all_log.logger.info("---帐号%s于%s已在%s发布评论---" % (account, last_time_str, task['group_id']))
                            continue
                    except KeyError:
                        pass
                    except ValueError:
                        pass
                    rd_num = random.randint(0, len(content_list) - 1)
                    content = content_list[rd_num]['content'].replace("\\r\\n", "").strip()
                    is_done,is_share,is_find = doComment(acc,task,content)
                    #未找到帖子
                    if not is_find:
                        break
                    if is_done:
                        done_num = int(task['done_num']) + 1
                        if int(task['nums']) > done_num:
                            update_sql = "update tb_post set done_num=done_num+1,accounts=concat(accounts,%s),content=concat(content,%s)"
                            if is_share:
                                update_sql += ",done_share=done_share+1"
                            update_sql += " where id=%s"
                            update_param = [account+"|",content+"|",task['id']]
                            mp.update(update_sql,update_param)
                        else:
                            update_sql = "update tb_post set done_num=%s,accounts=concat(accounts,%s),state='finish',finish_time=%s,content=concat(content,%s)"
                            if is_share:
                                update_sql += ",done_share=done_share+1"
                            update_sql += " where id=%s"
                            update_param = [task['nums'],account,datetime.now(), content,task['id']]
                            mp.update(update_sql, update_param)
                        all_log.logger.info("*****更新数据库成功*****")
                        all_log.logger.info("*****帐号%s执行完成*****%s"%(acc['account'],task['id']))
                        break
                    else:
                        all_log.logger.info("*****帐号%s未完成*****%s"%(acc['account'],task['id']))
        all_log.logger.info("-----任务列表%s执行结束-----"%num_list)
    else:
        all_log.logger.info("-----无可执行任务-----")


def login(account, pwd, ua):
    all_log.logger.info("~~~~~开始自动登录并保存cookies信息~~~~~")
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=" + ua)
    prefs = {
        'profile.default_content_setting_values': {
            'notifications': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.facebook.com/")
    sleep(1)
    try:
        driver.find_element_by_name("email").send_keys(account)
        driver.find_element_by_name("pass").send_keys(pwd)
        driver.find_element_by_name("pass").send_keys(Keys.ENTER)
        sleep(1)
        # while True:
        #     print(driver.get_cookies())
        #     print(ua)
        #     sleep(5)
        if driver.current_url == "https://www.facebook.com/?sk=welcome":
            all_log.logger.info("~~~~~登录成功~~~~~")
            config = configparser.RawConfigParser()
            config.read("fb-user.ini", encoding="utf-8")
            cookies = driver.get_cookies()
            config.set(account, "cookies", cookies)
            config.set(account, "user-agent", ua)
            config.write(open("fb-user.ini", "w"))
            return cookies
        else:
            error_log.logger.error("~~~~~%s登录失败~~~~~"%account)
            return None
    except Exception as e:
        traceback.print_exc()
        error_log.logger.error("~~~~~%s登录失败~~~~~"%account)
        return None
    finally:
        driver.quit()

def answerQuersion(task,driver):
    all_log.logger.info("-----开始回答%s问题-----"%task['group_id'])
    config = configparser.RawConfigParser()
    config.read("group-answer.ini", encoding="utf-8")
    try:
        for group in config:
            if task['group_id'] == group:
                a1 = config[group]['a1']
                a1_is_textarea = False
                a2 = config[group]['a2']
                a2_is_textarea = False
                try:
                    a3 = config[group]['a3']
                except:
                    a3 = None
                try:
                    a4 = config[group]['a4']
                except:
                    a4 = None
                #第一个问题是选择题
                if len(a1) == 1:
                    #选择第一个选项
                    if a1 == "1":
                        driver.find_element_by_xpath('//div[@role="radiogroup"]/div/div').click()
                    #选择第二个选项
                    else:
                        driver.find_element_by_xpath('//div[@role="radiogroup"]/div[2]/div').click()
                elif len(a1) == 2 and "|" in a1:
                    a1_label = a1.split("|")[0]
                    if a1_label == "1":
                        driver.find_element_by_xpath('//div[@aria-label="回答问题"]//label').click()
                    else:
                        num = int(a1_label) -1
                        driver.find_element_by_xpath('//div[@aria-label="回答问题"]//label/../../following-sibling::div['+str(num)+']//label').click()
                #第一个问题是问答题
                else:
                    a1_is_textarea = True
                    a1_answers = a1.split("|")
                    lens = len(a1_answers)
                    if lens > 1:
                        a1_answer = a1_answers[random.randint(0,lens-1)]
                    else:
                        a1_answer = a1
                    driver.find_element_by_xpath('//div[@aria-label="回答问题"]//textarea').send_keys(a1_answer)
                sleep(0.5)
                # 第二个问题是选择题
                if len(a2) == 1:
                    if a1_is_textarea:
                        if a2 == "1":
                            driver.find_element_by_xpath('//div[@role="radiogroup"]/div').click()
                        # 选择对应选项
                        else:
                            driver.find_element_by_xpath('//div[@role="radiogroup"]/div['+a2+']').click()
                    else:
                        if a2 == "1":
                            driver.find_element_by_xpath('//div[@role="radiogroup"]/../../../following-sibling::div[1]//div[@role="radiogroup"]/div/div').click()
                        else:
                            driver.find_element_by_xpath('//div[@role="radiogroup"]/../../../following-sibling::div[1]//div[@role="radiogroup"]/div['+a2+']/div').click()
                else:
                    a2_is_textarea = True
                    a2_answers = a2.split("|")
                    lens = len(a2_answers)
                    if lens > 1:
                        a2_answer = a2_answers[random.randint(0, lens - 1)]
                    else:
                        a2_answer = a2
                    if a1_is_textarea:
                        driver.find_element_by_xpath('//div[@aria-label="回答问题"]//textarea/../../../../following-sibling::div[1]//textarea').send_keys(a2_answer)
                    else:
                        driver.find_element_by_xpath('//div[@aria-label="回答问题"]//textarea').send_keys(a2_answer)
                sleep(0.5)
                #第三个问题
                if a3 is not None:
                    if a3 == "000":
                        driver.find_element_by_xpath(
                            '//div[@aria-label="回答问题"]//div[@role="dialog"]/div[2]/div/div[5]//input').click()
                    elif a3 == "textarea":
                        pass
                    else:
                        if len(a3) == 1:
                            if a1_is_textarea and a2_is_textarea:
                                if a3 == "1":
                                    driver.find_element_by_xpath('//div[@role="radiogroup"]/div').click()
                                # 选择对应选项
                                else:
                                    driver.find_element_by_xpath(
                                        '//div[@role="radiogroup"]/div[' + a3 + ']').click()
                            elif not a1_is_textarea and not a2_is_textarea:
                                if a3 == "1":
                                    driver.find_element_by_xpath(
                                        '//div[@role="radiogroup"]/../../../following-sibling::div[2]//div[@role="radiogroup"]/div/div').click()
                                else:
                                    driver.find_element_by_xpath(
                                        '//div[@role="radiogroup"]/../../../following-sibling::div[2]//div[@role="radiogroup"]/div[' + a3 + ']/div').click()
                            else:
                                if a3 == "1":
                                    driver.find_element_by_xpath(
                                        '//div[@role="radiogroup"]/../../../following-sibling::div[1]//div[@role="radiogroup"]/div/div').click()
                                else:
                                    driver.find_element_by_xpath(
                                        '//div[@role="radiogroup"]/../../../following-sibling::div[1]//div[@role="radiogroup"]/div[' + a3 + ']/div').click()
                        else:
                            a3_answers = a3.split("|")
                            lens = len(a3_answers)
                            if lens > 1:
                                a3_answer = a3_answers[random.randint(0, lens - 1)]
                            else:
                                a3_answer = a3
                            if a1_is_textarea and a2_is_textarea:
                                driver.find_element_by_xpath('//div[@aria-label="回答问题"]//textarea[3]').send_keys(
                                    a3_answer)
                            elif a1_is_textarea or a2_is_textarea:
                                driver.find_element_by_xpath('//div[@aria-label="回答问题"]//textarea[2]').send_keys(a3_answer)
                            else:
                                driver.find_element_by_xpath('//div[@aria-label="回答问题"]//textarea').send_keys(a3_answer)
                    sleep(0.5)
                # 第四个问题
                if a4 is not None:
                    driver.find_element_by_xpath(
                        '//div[@aria-label="回答问题"]//div[@role="dialog"]/div[2]/div/div[6]//input').click()
                    sleep(0.5)
                driver.find_element_by_xpath('//div[@role="dialog"][last()]/div[3]/span[2]').click()
                sleep(0.5)
                break
        all_log.logger.info("-----回答问题结束-----")
    except Exception as e:
        traceback.print_exc()
        error_log.logger.error("-----%s回答问题报错-----"%task['group_id'])
    finally:
        driver.quit()

def doComment(acc,task,content):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=" + acc['user-agent'])
    # prefs = {
    #     'profile.default_content_setting_values': {
    #         'notifications': 2
    #     }
    # }
    # options.add_experimental_option('prefs', prefs)
    # options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # options.add_argument("log-level=3")
    # options.add_argument('blink-settings=imagesEnabled=false')
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://www.baidu.com/")
        sleep(1000)
        if type('') is type(acc['cookies']):
            cookie_list = eval(acc['cookies'])
        else:
            cookie_list = acc['cookies']
        for cookie in cookie_list:
            driver.add_cookie(cookie_dict=cookie)
        driver.get("https://www.facebook.com/search/groups/?q=%s"%task['group_id'])
        # sleep(5000)
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  '//div[@id="BrowseResultsContainer"]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/button')))
            group_state = driver.find_element_by_xpath(
                '//div[@id="BrowseResultsContainer"]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/button').text
        except:
            try:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      '//div[@id="BrowseResultsContainer"]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/a')))
                group_state = driver.find_element_by_xpath(
                    '//div[@id="BrowseResultsContainer"]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/a').text
            except:
                error_log.logger.error("-----查找群组%s出错-----" % task['group_id'])
                driver.quit()
                return False,False,True
        all_log.logger.info("*****state:%s*****"%group_state)
        if group_state == "请求已发送":
            all_log.logger.info("-----%s加入群组请求已发送-----" % acc['account'])
            driver.quit()
            return False,False,True
        elif group_state == "加入":
            driver.find_element_by_xpath(
                '//div[@id="BrowseResultsContainer"]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/a').click()
            try:
                WebDriverWait(driver, 8).until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      '//div[contains(@aria-label,"回答问题")]')))
                answerQuersion(task,driver)
            except:
                error_log.logger.error("-----%s无需回答问题-----"% task['group_id'])
            driver.quit()
            return False,False,True
        elif group_state == "已加入":
            try:
                driver.find_element_by_xpath('//*[@id="BrowseResultsContainer"]/div[1]//a').click()
                WebDriverWait(driver, 8).until(
                    EC.visibility_of_element_located((By.NAME, 'query')))
                driver.find_element_by_name("query").send_keys(task['keyword'])  # PQSTISPT 50CQ5GQI
                driver.find_element_by_xpath('//span[@class="uiSearchInput"]/span/button').click()
                try:
                    WebDriverWait(driver, 8).until(
                        EC.visibility_of_element_located((By.XPATH, '//div[@id="BrowseResultsContainer"]')))
                except TimeoutException:
                    error_log.logger.error("-----%s未找到%s的帖子,此任务跳过-----"%(task['group_id'],task['keyword']))
                    return False,False,False
                try:
                    driver.find_element_by_xpath(
                        '//*[@id="BrowseResultsContainer"]/div/div/div/div/div/div/div/div/div[3]/div/div/div[3]//a').click()
                except:
                    driver.find_element_by_xpath(
                        '//div[@data-testid="results"]/div/div/div/div/div/div/div/div/div[3]/div/div/div[3]//a').click()
                WebDriverWait(driver, 8).until(
                    EC.visibility_of_element_located((By.XPATH, '//form[@class="commentable_item"]')))
                driver.find_element_by_xpath('//form[@class="commentable_item"]/div/div[2]/div[2]/div//a').click()
                sleep(1)
                all_log.logger.info("*****点赞成功*****")
                driver.find_element_by_xpath('//form[@class="commentable_item"]/div/div[2]/div[2]/div/span[2]/a').click()
                WebDriverWait(driver, 8).until(
                    EC.visibility_of_element_located((By.XPATH, '//div[contains(@aria-label,"写评论...")]')))
                driver.find_element_by_xpath('//div[contains(@aria-label,"写评论...")]').send_keys(content)
                sleep(1)
                driver.find_element_by_xpath('//div[contains(@aria-label,"写评论...")]').send_keys(Keys.ENTER)
                sleep(1)
                all_log.logger.info("*****评论成功*****")
                is_share = False
                if task['share_num'] > task['done_share']:
                    try:
                        driver.find_element_by_xpath('//a[@title="发送给好友或发布到你的时间线上。"]').click()
                        WebDriverWait(driver, 8).until(
                            EC.visibility_of_element_located((By.XPATH, '//ul[@role="menu"]')))
                        driver.find_element_by_xpath('//ul[@role="menu"]/li').click()
                        is_share = True
                        all_log.logger.info("*****分享成功*****")
                        sleep(1)
                    except Exception as e:
                        traceback.print_exc()
                        error_log.logger.error("*****%s分享失败-此贴无分享功能*****"% task['group_id'])
                else:all_log.logger.info("*****无需分享*****")
                config = configparser.RawConfigParser()
                config.read("fb-user.ini", encoding="utf-8")
                config.set(acc['account'], task['group_id'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                config.set(acc['account'], "cookies", driver.get_cookies())
                config.write(open("fb-user.ini", "w"))
                sleep(1)
                all_log.logger.info("*****更新帐号配置文件成功*****")
                all_log.logger.info("*****帐号%s执行完成*****"%acc['account'])
                return True,is_share,True
            except Exception as e:
                traceback.print_exc()
                error_log.logger.error("*****帐号%s执行失败*****"%acc['account'])
                driver.quit()
                return False,False,True
    except:
        traceback.print_exc()
        return False, False, True
    finally:
        driver.quit()

def filter_str(desstr, restr=''):
    # 过滤除中英文及数字及英文标点以外的其他字符
    res = re.compile("[^\u4e00-\u9fa5^. !//_,$&%^*()<>+\"'?@#-|:~{}+|—^a-z^A-Z^0-9]")
    return res.sub(restr, desstr)

if __name__ == "__main__":
    # getTask()
    groupTask()