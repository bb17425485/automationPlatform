from selenium import webdriver
from selenium.webdriver.chrome.options import Options



chrome_options = Options()
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:5003")
# cookies = [{'domain': '.facebook.com', 'expiry': 1601998950, 'httpOnly': False, 'name': 'wd', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1366x614'}, {'domain': '.facebook.com', 'httpOnly': False, 'name': 'presence', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'EDvF3EtimeF1601394131EuserFA21B54872633192A2EstateFDutF1601394131780CEchF_7bCC'}, {'domain': '.facebook.com', 'expiry': 1601484125, 'httpOnly': True, 'name': 'spin', 'path': '/', 'secure': True, 'value': 'r.1002739988_b.trunk_t.1601394125_s.1_v.2_'}, {'domain': '.facebook.com', 'expiry': 1663827647, 'httpOnly': True, 'name': 'sb', 'path': '/', 'secure': True, 'value': 'tZdpX_7xk7tIMKjadxwYy-0q'}, {'domain': '.facebook.com', 'expiry': 1608531645, 'httpOnly': True, 'name': 'fr', 'path': '/', 'secure': True, 'value': '1jpSJmW6aka8Sk2Au.AWX8se5maX9v96T1stEhClBF6SI.BfaZe1.rX.AAA.0.0.BfaZe8.AWWCvlwe'}, {'domain': '.facebook.com', 'expiry': 1632291646, 'httpOnly': True, 'name': 'xs', 'path': '/', 'secure': True, 'value': '17%3Au433raFhoECAXQ%3A2%3A1600755644%3A-1%3A-1'}, {'domain': '.facebook.com', 'expiry': 1632291646, 'httpOnly': False, 'name': 'c_user', 'path': '/', 'secure': True, 'value': '100054872633192'}, {'domain': '.facebook.com', 'expiry': 1663827642, 'httpOnly': True, 'name': 'datr', 'path': '/', 'secure': True, 'value': 'tZdpX8JHRgi2PRQghMmazBpG'}]
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://amz.do/")

# for cookie in cookies:
#     driver.add_cookie(cookie_dict=cookie)
# driver.get("https://www.facebook.com")
