from nonebot.adapters.cqhttp import Message
from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import requests
from aiocqhttp.exceptions import Error as CQHttpError
from nonebot.adapters.cqhttp.message import MessageSegment
import httpx
from nonebot.log import logger
import json


da = on_keyword({'美腿'})
@da.handle()
async def j(bot: Bot, event: Event, state: False):
    msg = await ji()
    try:
        await da.send(Message(msg))
    except CQHttpError:
        pass

async def ji():
    url = 'https://img1.baidu.com/it/u=3246628741,3439955235&fm=26&fmt=auto'
    da = requests.get(url).text
    pic = f'[CQ:image, file={da}]'
    return pic