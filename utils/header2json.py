#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :header2json.py
@说明        :
@时间        :2022/04/05 17:25:59
@作者        :shitianfang
@版本        :1.0
'''

import json

t="""Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Host: capi.tianyancha.com
Origin: https://www.tianyancha.com
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
User-Agent: Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36 Edg/45.3.4.4958
accept: */*
accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
version: TYC-Web
x-auth-token: eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTU0NzM2MjcwMyIsImlhdCI6MTY0OTA3OTIwMywiZXhwIjoxNjUxNjcxMjAzfQ.Ka52eg_W8fHDpoTHVdd8OWINIS38izlR8pGjR7Zz6-VTXxWwXQ_tg8jRhmWUKTKcUpA6gCcywHpEigdCM6uS9w
x-tycid: 22d85440b0b311ec9fa889bf4263f7c4"""

d={}
for l in t.split("\n"):
    print(l)
    n,v = l.split(":",maxsplit=1)
    d[n]=v

with open("t.json","w") as f:
    json.dump(d,f)