#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File       :   app.py
@Time       :   2024/5/31 13:36
@Author     :   xunhanliu
@Desc       :   
"""

import os
import pickle
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()

INDEX_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

CHROME_OPTIONS_DEFAULT_USER_AGENT = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, " \
                                    "like Gecko) Chrome/95.0.4638.69 Safari/537.36"
CHROME_OPTIONS_ADD_ARGUMENTS = [
    "--disable-gpu",  # 谷歌文档提到需要加上这个属性来规避bug
    "--disable-dev-shm-usage",  # 大量渲染时候写入/tmp而非/dev/shm
    # "--window-size=1920,1200",
    "--disk-cache-dir="+CACHE_PATH,  # 指定cache路径
    "--disk-cache-size=1073741824",
    "--media-cache-size=1073741824",
    "--disable-blink-features=AutomationControlled",  # 消除启动特征防止反爬
    "--force-dev-mode-highlighting",  # 是否强制开发者模式扩展突出显示
    # "-–single-process",  # 单进程运行
    CHROME_OPTIONS_DEFAULT_USER_AGENT,

]
COOKIE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookie.pkl")
for item in CHROME_OPTIONS_ADD_ARGUMENTS:
    chrome_options.add_argument(item)

driver = webdriver.Chrome(options=chrome_options)
driver.get(INDEX_FILE)


def text_not_equal(locator, text_):
    def _predicate(driver):
        try:
            element_text = driver.find_element(*locator).text
            return text_ != element_text
        except InvalidSelectorException as e:
            raise e
        except StaleElementReferenceException:
            return False

    return _predicate


iframe_ids = ["doubao", "tiangong", "yiyan", "chatglm", "chatgpt"]
iframe_send_css = {"doubao": ".semi-input-textarea", "tiangong": ".el-input__inner", "yiyan": "#dialogue-input",
                   "chatglm": ".input-box-inner textarea", "chatgpt": "#prompt-textarea"}

# 开始恢复cookie
if os.path.exists(COOKIE_FILE):
    with open(COOKIE_FILE, "rb") as f:
        driver.delete_all_cookies()
        cookie_data = pickle.load(f)
        for id_iframe in iframe_ids:
            if id_iframe not in cookie_data:
                continue
            _iframe = driver.find_element(By.ID, id_iframe)
            driver.switch_to.frame(_iframe)
            # driver.get(iframe_url[id_iframe])

            for item in cookie_data[id_iframe]:
                driver.add_cookie(item)
            # driver.get(iframe_url[id_iframe])
            driver.switch_to.parent_frame()
    driver.refresh()

while True:
    try:
        WebDriverWait(driver, 10).until(
            text_not_equal((By.ID, "send-button"), "发送")
        )

        if driver.find_element(By.ID, "send-button").text == "保存中":
            print("保存中")
            with open(COOKIE_FILE, "wb") as f:
                cookie_data = {}
                for id_iframe in iframe_ids:
                    _iframe = driver.find_element(By.ID, id_iframe)
                    driver.switch_to.frame(_iframe)
                    cookie_list = driver.get_cookies()
                    cookie_data[id_iframe] = cookie_list
                    driver.switch_to.parent_frame()
                pickle.dump(cookie_data, f)

            time.sleep(3)
            continue
        # 开始后续的查找元素的操作
        # 获取用户的输入
        e_text_input = driver.find_element(By.ID, "text-area")
        text_input = e_text_input.get_attribute("value")
        e_text_input.clear()

        for id_iframe in iframe_ids:
            _iframe = driver.find_element(By.ID, id_iframe)
            driver.switch_to.frame(_iframe)
            try:
                try:
                    elem = driver.find_element(By.CSS_SELECTOR, iframe_send_css[id_iframe])
                except NoSuchElementException:
                    if id_iframe == "tiangong":
                        try:
                            elem = driver.find_element(By.CSS_SELECTOR, ".el-textarea__inner")
                            elem.send_keys(text_input)
                            btn = driver.find_element(By.CSS_SELECTOR, ".sendDiv")
                            btn.click()
                            continue
                        except Exception as e:
                            continue
                    else:
                        elem = None
                if not elem:
                    continue
                # elem.clear()
                elem.send_keys(text_input)
                if id_iframe == "yiyan":
                    btn = driver.find_element(By.CSS_SELECTOR, ".VAtmtpqL")  # 一言需要额外点一下
                    btn.click()
                else:
                    elem.send_keys(Keys.RETURN)
            except Exception as e:
                print(e)
            finally:
                driver.switch_to.parent_frame()
    except Exception as e:
        pass
