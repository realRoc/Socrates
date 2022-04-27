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



evaluation = on_command('eval', rule=to_me(), priority=4)
@evaluation.handle()
async def handle_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state['input'] = args

@evaluation.got('input', prompt='您对上一轮对话的评价是？')
async def handle_eval(bot: Bot, event: Event, state: T_State):
    user_id = event.get_user_id()
    sql_select = f'select Input, Output from history \
            where User_ID=\'{user_id}\' \
            order by Update_Time desc limit 1'
    conn = mysql.DbOperation(host='localhost', user='root', password='961224', database='socrates')
    
    comment = state['input']
    senti = await sentiment_analysis(comment)
    label = list(senti.keys())[0]
    label2message = {
            'positive': '感谢您的好评！',
            'negative': '收到您的差评！我会继续努力的！',
            'neutral': '感谢您的评价！已保存评价至数据库~'
        }
    
    try:
        Input, Output = conn.select(sql_select)[0]     
    except:
        await evaluation.send(Message('历史数据获取失败...'))
    
    sql_update = f'insert into data(User_ID, Input, Output, Label, Comment) \
            values (\'{user_id}\', \'{Input}\', \'{Output}\', \'{label}\', \'{comment}\');'
    
    try:
        conn.update(sql_update)
        await evaluation.send(Message(label2message[label]))
    except CQHttpError:
        await evaluation.send(Message('存储对话失败...'))
        
    conn.close()


async def sentiment_analysis(text):
    senti = SentimentAnalysis()
    senti = senti.analysis(text)
    return senti

