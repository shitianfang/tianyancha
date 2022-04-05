#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :tianyancha.py
@说明        :
@时间        :2022/04/05 17:25:29
@作者        :shitianfang
@版本        :1.0
'''

from .base import ParserBase
from config.tianyancha import auth_headers
from pyquery import PyQuery as pq
import aiohttp
import json


class Company(ParserBase):

    bussiness_api = "https://capi.tianyancha.com/cloud-dim-facade/company/export?dimKey=baseInfo&gid={gid}"

    base_query = {
        "phone": "#company_web_top > div.box.-company-box.-company-claimed > div.content > div.detail > div:nth-child(2) > div.in-block.sup-ie-company-header-child-1.copy-info-box > span > span.copy-it.info-need-copy._phone",
        "email": "#company_web_top > div.box.-company-box.-company-claimed > div.content > div.detail > div:nth-child(2) > div.in-block.sup-ie-company-header-child-2.copy-info-box > span > span.email.copy-it.info-need-copy._email",
        "url": "#company_web_top > div.box.-company-box.-company-claimed > div.content > div.detail > div.f0.clearfix.mb0.address > div.in-block.sup-ie-company-header-child-1 > a.company-link",
        "address": "#company_web_top > div.box.-company-box.-company-claimed > div.content > div.detail > div.f0.clearfix.mb0.address > div.in-block.sup-ie-company-header-child-2.copy-component-box > span > div > div > div",
        "introduce": "#company_web_top > div.box.-company-box.-company-claimed > div.content > div.detail > div.summary.mt8 > div > div",
    }

    product_query = "#_container_product > table > tbody > tr"
    product_api = "https://www.tianyancha.com/next/api/product/detail?uuid={uuid}"

    jingpin_list_page = "https://www.tianyancha.com/pagination/jingpin.xhtml?ps=30&pn={page}&id={gid}"

    @classmethod
    async def parse_business_info(cls, context):
        headers = auth_headers(context["cookies"])
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.bussiness_api.format(gid=context['gid']), headers=headers) as response:
                return await response.json()

    @classmethod
    def parse_base_info(cls, context):
        base_info = {}
        doc = context["doc"]
        for key, query in cls.base_query.items():
            base_info[key] = doc(query).text()
        return base_info

    @classmethod
    async def parse_product_list(cls, context):
        product_list = []
        doc = context["doc"]
        browser = context["browser"]
        parse_page = await browser.newPage()
        for product in doc(cls.product_query).items():
            uuid = product("td:nth-child(6) > a").attr("href").split("/")[-1]
            await parse_page.goto(cls.product_api.format(uuid=uuid))
            brief = json.loads(await parse_page.plainText())["data"]["result"]["data"]["brief"]
            product_list.append({
                "name": product("td:nth-child(2)").text(),
                "category": product("td:nth-child(4)").text(),
                "field": product("td:nth-child(5)").text(),
                "brief": brief
            })
        return product_list

    @classmethod
    async def parse_competitive_product(cls, context):
        cp_list = []
        page = 1
        browser = context["browser"]
        parse_page = await browser.newPage()
        while True:
            await parse_page.goto(cls.jingpin_list_page.format(gid=context['gid'],page=page))
            html = await parse_page.content()
            doc = pq(html)
            count = 0
            for cp in doc("body > div > table > tbody > tr").items():
                cp_list.append({
                    "name": cp("td:nth-child(2)").text(),
                    "finance": cp("td:nth-child(3)").text(),
                    "estinmation": cp("td:nth-child(4)").text(),
                    "register_date": cp("td:nth-child(5)").text(),
                    "tag": cp("td:nth-child(6)").text(),
                    "region": cp("td:nth-child(7)").text(),
                    "brief": cp("td:nth-child(8)").text(),
                    "company": cp("td:nth-child(9)").text(),
                })
                count += 1
            if count <= 10:
                break
            page += 1
        return cp_list