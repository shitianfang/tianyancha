#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :tianyancha.py
@说明        :
@时间        :2022/04/05 17:25:41
@作者        :shitianfang
@版本        :1.0
'''

import asyncio
import json
from pyppeteer import launch
from pyquery import PyQuery as pq
from pathlib import Path
from parser.tianyancha import Company
import pickle


class TianYanCha:
    def __new__(cls, *args, **kwargs):
        """ Singleton Pattern """
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
        self.login_url = "https://www.tianyancha.com/login"
        self.login_redirect_url = "https://www.tianyancha.com/"
        self.company_url = "https://www.tianyancha.com/company/{gid}"
        self.view_port = {'width': 1920, 'height': 1080}
        self.cookies_path = "cookies/tianyancha.cookies"

    def has_cookies(self):
        return Path(self.cookies_path).exists()

    def load_cookies(self):
        with open(self.cookies_path, "rb") as f:
            self.cookies = pickle.load(f)

    def save_cookies(self):
        with open(self.cookies_path, "wb") as f:
            pickle.dump(self.cookies, f, 0)

    async def login(self, save=True):
        """Login and save cookies

        Args:
            save (bool, optional): Save Cookies. Defaults to True.
        """
        login_browser = await launch(headless=False)
        login_page = await login_browser.newPage()
        await login_page.setViewport(self.view_port)
        await login_page.goto(self.login_url)
        await login_page.waitForNavigation()
        print("Resize Chrome Window to Login")
        while True:
            if login_page.url == self.login_redirect_url:
                self.cookies = await login_page.cookies()
                await login_browser.close()
                if save:
                    self.save_cookies()
                break
            await asyncio.sleep(1)

    async def company(self, gid):
        """Fetch TianYanCha Company Data

        Args:
            gid (int): Company id

        Returns:
            dict: All company paser data
        """
        company_page = await self.browser.newPage()
        await company_page.setViewport(self.view_port)
        if hasattr(self, "cookies"):
            await company_page.setCookie(*self.cookies)
        await company_page.goto(self.company_url.format(gid=gid))
        await company_page.waitForNavigation() # wait page completed
        company_html = await company_page.content()
        result = await Company.parse(
            {"gid": gid,
             "cookies": self.cookies,
             "doc": pq(company_html),
             "browser": self.browser
             })
        return result

    def export(self, data, export_path="out.json"):
        with open(export_path, "w") as f:
            json.dump(data, f)

    async def launch(self, login=False):
        if login:
            if self.has_cookies():
                self.load_cookies()
            else:
                await self.login()
        self.browser = await launch()

    async def close(self):
        await self.browser.close()
