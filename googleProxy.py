# -*- codeing = utf-8 -*-
# @Time : 2020/10/12 11:42
# @Author : Cj
# @File : googleProxy.py
# @Software : PyCharm


from selenium import webdriver
from time import sleep
import string,zipfile

# 打包Google代理插件
def create_proxyauth_extension(proxy_host, proxy_port, proxy_username, proxy_password, scheme='http', plugin_path=None):
    if plugin_path is None:
        # 插件地址
        plugin_path = 'D:/Python/vimm_chrome_proxyauth_plugin2.zip'

    manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

    background_js = string.Template(
        """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                  },
                  bypassList: ["foobar.com"]
                }
              };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path

# 填写主机地址，端口，账号，密码
proxyauth_plugin_path = create_proxyauth_extension(
    proxy_host="196.240.104.107",
    proxy_port=12345,
    proxy_username="pethan",
    proxy_password="52renren"
)

# 测试
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_extension('D:/Python/vimm_chrome_proxyauth_plugin2.zip')
driver = webdriver.Chrome(options=options)
driver.get("https://www.baidu.com/")
sleep(10000)