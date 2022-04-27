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



ACCESS_TOKEN = "24.cbb33bc9567d930dfa6bfdbf181de695.2592000.1641788166.282335-25309873"
# API_KEY = "qsxagODihhOhGs7Rd2zx9KOm"
# SECRET_KEY = "UF36c5Pp3FSytrhdkc3fYr5Yl1m3dnyj"

summary = on_command('summ', rule=to_me(), priority=4)
@summary.handle()
async def handle_receive(bot: Bot, event: Event, state: T_State):
    user_id = event.get_user_id()
    sql_select = f'select History from history \
            where User_ID=\'{user_id}\' \
            order by Update_Time desc limit 1'
    conn = mysql.DbOperation(host='localhost', user='root', password='961224', database='socrates')
    
    try:
        history = conn.select(sql_select)[0][0]
        msg = await get_summ_answer(history)
        await summary.send(Message(msg))
    except:
        await summary.send(Message('调用文心ERNIE大模型失败...'))
    
    conn.close()


async def get_summ_answer(text_str):
    MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/text_gen/Socrates_Summ"
    request_url = "{}?access_token={}".format(MODEL_API_URL, ACCESS_TOKEN)
    PARAMS = {"max_gen_len": 128}
    PARAMS["text"] = f'历史记录：{text_str}摘要：'

    response = requests.post(url=request_url, json=PARAMS)
    response_json = response.json()
    try:
        return response_json['result']['content']
    except KeyError:
        return False

