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


# TODO 相同的输入Input是否需要更新history？ 
    # - 测试表明此为次要需求
# TODO 同一user根据Input对history进行分类 -阅读理解/文本分类
    # solution 1：jieba分词，计算word2vec similarity
        # - word2vec只能计算句子相似度，无法处理相关度的需求
    # solution 2：计算Attention
# TODO 段落总结：对于>512的history会丢失历史信息的问题
    # solution 1：摘要总结
        # -猜测：后面输入的attention weight比较大


# socrates = on_command('@苏格拉底', rule=to_me(), priority=1, temp=True)
socrates = on_message(rule=to_me(), priority=1)
@socrates.handle()
async def handle_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state['input'] = args

@socrates.got('input', prompt='年轻人，你想询问什么？')
async def handle_input(bot: Bot, event: Event, state: T_State):
    conn = mysql.DbOperation(host='localhost', user='root', password='961224', database='socrates')
    user_id = event.get_user_id()
    date_time = datetime.now().strftime('%y-%m-%d %H:%M:%S')
    sql_select = f'select History from history \
            where User_ID=\'{user_id}\' \
            order by Update_Time desc \
            limit 1'
    Input = state['input']
    try:
        history = conn.select(sql_select)[0][0][-512:]
        msg = await get_socrates_answer(history)
        history += '\n' + Input + '\n' + msg
    except (TypeError, IndexError):
        history = Input
        msg = await get_socrates_answer(history)
        history += '\n' + msg
    sql_update = f'insert into history(User_ID, Input, Output, Update_Time, History) \
            values (\'{user_id}\', \'{Input}\', \'{msg}\', \'{date_time}\', \'{history}\');'
    conn.update(sql_update)
    conn.close()
    
    try:
        await socrates.send(Message(msg))
        await socrates.send(Message(history))
    except CQHttpError:
        pass

async def get_socrates_answer(text_str):
    MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/text_gen/Socrates_V1"
    ACCESS_TOKEN = "24.cbb33bc9567d930dfa6bfdbf181de695.2592000.1641788166.282335-25309873"
    # API_KEY = "qsxagODihhOhGs7Rd2zx9KOm"
    # SECRET_KEY = "UF36c5Pp3FSytrhdkc3fYr5Yl1m3dnyj"

    request_url = "{}?access_token={}".format(MODEL_API_URL, ACCESS_TOKEN)
    PARAMS = {"max_gen_len": 128}
    PARAMS["text"] = f'问题：{text_str}\t反问：'

    response = requests.post(url=request_url, json=PARAMS)
    response_json = response.json()
    # response_str = json.dumps(response_json, indent=4, ensure_ascii=False)

    return response_json['result']['content']

