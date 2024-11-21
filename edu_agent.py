#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/4/10 下午5:56
# @Author  : Siyue
# @Site    : 
# @File    : IP_anget_pool.py
# @Software: PyCharm

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""使用requests请求代理服务器
请求http和https网页均适用
"""

import requests
import random

from bs4 import BeautifulSoup


from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Frame, sync_playwright


def request_by_ip_agent():
    # reqeust_url = "http://dev.kdlapi.com/testproxy"  # 要访问的目标网页

    # 获取IP代理的API接口，返回格式为json
    api_url = "https://dps.kdlapi.com/api/getdps/?secret_id=ozj4wppqtww5x4cuersk&signature=148si07znb5dw5rn9lajjws2b2h6egld&num=1&pt=1&sep=1"

    # 获取API接口返回的代理IP
    proxy_ip = requests.get(api_url).text

    # # 用户名密码认证(私密代理/独享代理)
    # username = "d3433101710"
    # password = "us8bel5b"
    # proxies = {
    #     "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    #     "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
    # }
    proxies = {
        'server': proxy_ip,
        'username': 'd3428182723',
        'password': '9vfvzuap'
    }
    return proxies


def test_get_ip(proxies):
    # proxies = request_by_ip_agent()
    headers = {
        "Accept-Encoding": "Gzip",  # 使用gzip压缩传输数据让访问更快
    }

    # 这一部分，为了看看自己获取的代理IP
    r = requests.get('http://dev.kdlapi.com/testproxy', proxies=proxies, headers=headers)
    print(r.status_code)  # 获取Response的返回码
    print(r.content)  # 获取Response的返回码


def request_chsi_by_request(request_url, proxies):
    # 真正请求学信网
    # proxies = request_by_ip_agent()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Ch-Ua-Platform': 'macOS',
        'Pragma': 'no-cache',
        'Host': 'www.chsi.com.cn'
    }
    r = requests.get(request_url, proxies=proxies, headers=headers)
    print(r.status_code)  # 获取Response的返回码

    if r.status_code == 200:
        r.enconding = "utf-8"  # 设置返回内容的编码
        print(r.content)  # 获取页面内容
        return r.content
    else:
        print(r.status_code)
        print(r.content)
        return None


def request_chsi_by_playwriht(playwright, reqeust_url, proxies):
    # proxies = request_by_ip_agent()
    print(f"proxies: {proxies}")

    # browser = playwright.chromium.launch(headless=True)  # 设置为 False 以在可见窗口中运行
    browser = playwright.firefox.launch(headless=True, proxy=proxies)  # 设置为 False 以在可见窗口中运行
    # browser = playwright.chromium.launch(headless=False)

    context = browser.new_context()
    # 导航到网页
    page = context.new_page()

    page.goto(reqeust_url)
    page.wait_for_timeout(3500)  # 等待2秒作为示例

    # 打印整个页面的 HTML 内容
    # print("\n\nPage HTML:")
    # print(page.content())

    # 等待页面加载完成或进行其他操作...
    # ...
    page_result = page.content()
    # 关闭浏览器
    browser.close()
    return page_result


def parse_html(res_html):
    soup = BeautifulSoup(res_html, 'html.parser')
    all_infos = soup.find_all('div', class_='report-info-item')
    print(all_infos)

    import re
    result = {}
    for info in all_infos:
        print("\n##############")
        info_str = str(info)
        print(info_str)
        key = re.findall(r'<div class="label">(.*?)</div>', info_str)
        print(key)

        if 'div class="value long"' in info_str:
            value = re.findall(r'<div class="value long">(.*?)</div>', info_str)
        else:  # "value" in str(info)
            value = re.findall(r'<div class="value">(.*?)</div>', info_str)
        print(value)
        result[key[0]] = value[0]
    is_student = False
    edu_history_id = None
    if '学籍状态' in result:
        if "注册学籍" in result['学籍状态']:
            print(f"real_name: {result['姓名']}")
            print(f"colloge: {result['院校']}")
            print(f"degree: {result['层次']}")
            print(f"major: {result['专业']}")


if __name__ == "__main__":
    vcode_list = ['ACUT2590BBX710G6', '828264861563', 'A33JL8RH0S0U7342', 'AR432EWPSPL20GHK', 'A630GCH8P91HGAL6', 'AM7B45T2AY4L1Q5E']
    import random

    vcode = random.choice(vcode_list)
    reqeust_url = f'https://www.chsi.com.cn/xlcx/bg.do?vcode={vcode}&srcid=bgcx'
    proxies = request_by_ip_agent()
    print(proxies)
    test_get_ip(proxies)
    print('VVVVVVVVVVVVVVVVVVV')
    # request_chsi_by_request(reqeust_url)

    with sync_playwright() as p:
        page = request_chsi_by_playwriht(p, reqeust_url, proxies)
        # print(f"\n\n\n\npage:\n{page}")

    parse_html(page)
