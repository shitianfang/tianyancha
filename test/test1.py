#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :test1.py
@说明        :
@时间        :2022/04/05 17:25:51
@作者        :shitianfang
@版本        :1.0
'''

from spider.tianyancha import TianYanCha
import asyncio

async def start():
    await TianYanCha().launch()
    await TianYanCha().company(1271389459)
    await TianYanCha().close()


loop = asyncio.new_event_loop()
loop.create_task(start())
loop.run_forever()