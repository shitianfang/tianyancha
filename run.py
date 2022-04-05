import asyncio
from spider.tianyancha import TianYanCha


async def start():
    await TianYanCha().launch(login=True)
    data = await TianYanCha().company(1271389459)
    TianYanCha().export(data,"1271389459.json")
    await TianYanCha().close()
    print("ok")


loop = asyncio.new_event_loop()
loop.create_task(start())
loop.run_forever()