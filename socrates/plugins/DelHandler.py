from nonebot.adapters.cqhttp import Message
from nonebot import on_command
from nonebot.plugin import on_message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import requests
from aiocqhttp.exceptions import Error as CQHttpError
from nonebot.adapters.cqhttp.message import MessageSegment
import httpx
from nonebot.log import logger
import json
from datetime import datetime
from tools import mysql
from tools import SentimentAnalysis



delete = on_command('del', rule=to_me(), priority=4)
@delete.handle()
async def handle_receive(bot: Bot, event: Event, state: T_State):
    user_id = event.get_user_id()
    sql_select = f'delete from history \
            where User_ID=\'{user_id}\''
    conn = mysql.DbOperation(host='localhost', user='root', password='961224', database='socrates')
    
    try:
        conn.delete(sql_select)
        await delete.send(Message('啊哦...我好像失忆了...'))
    except:
        await delete.send(Message('出了点小问题...等等你是打算让我失忆吗？'))
    
    conn.close()

