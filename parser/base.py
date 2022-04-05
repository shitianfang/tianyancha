from email import header


#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :base.py
@说明        :
@时间        :2022/04/05 17:25:15
@作者        :shitianfang
@版本        :1.0
'''



from asyncio.coroutines import iscoroutine


class ParserBase:
    @classmethod
    async def parse(cls, context):
        """Call all start with 'parse_' classmethod

        Args:
            context (dict): Pass parse classmethod data

        Returns:
            dict: All parse data, key named classmethod remove 'parse_'
        """
        result = {}
        for name, value in vars(cls).items():
            if isinstance(value, classmethod) and name.startswith("parse_"):
                if iscoroutine((parse_result := getattr(cls, name)(context))):
                    result[name[6:]] = await parse_result
                    print(result[name[6:]])
                else:
                    result[name[6:]] = parse_result
                    print(result[name[6:]])
        return result
