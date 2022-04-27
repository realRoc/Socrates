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
from tools import TextRankSummarization


# TODO 相同的输入Input是否需要更新history？ 
    # - 测试表明此为次要需求
# ✔ 同一user根据Input对history进行分类 -阅读理解/文本分类
    # solution 1：jieba分词，计算word2vec similarity ××× word2vec只能计算句子相似度，无法处理相关度的需求
    # solution 2：计算Attention ××× Pending
    # solution 3：百度文本分类服务（已实现）
# TODO 段落总结：对于>512的history会丢失历史信息的问题 ==> 构建用户画像
    # solution 1：摘要总结
        # -猜测：后面输入的attention weight比较大

ACCESS_TOKEN = "24.cbb33bc9567d930dfa6bfdbf181de695.2592000.1641788166.282335-25309873"
# API_KEY = "qsxagODihhOhGs7Rd2zx9KOm"
# SECRET_KEY = "UF36c5Pp3FSytrhdkc3fYr5Yl1m3dnyj"

socrates = on_message(rule=to_me(), priority=5)
@socrates.handle()
async def handle_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state['input'] = args

@socrates.got('input', prompt='年轻人，你想询问什么？')
async def handle_input(bot: Bot, event: Event, state: T_State):
    LABELS = ['Label_Material', 'Label_Growth', 'Label_Emotion']
    user_id = event.get_user_id()
    date_time = datetime.now().strftime('%y-%m-%d %H:%M:%S')
    Input = state['input']
    label_scores = await get_topic_classify(Input)
    
    sql_select = f'select Input, History, Label_Material, Label_Growth, Label_Emotion from history \
            where User_ID=\'{user_id}\''
    for i, score in enumerate(label_scores):
        if score > 0:
            sql_select += f' and {LABELS[i]}>0'
        else:
            sql_select += f' and {LABELS[i]}<=0'
    sql_select += ' order by Update_Time desc limit 1'
    
    conn = mysql.DbOperation(host='localhost', user='root', password='961224', database='socrates')
    
    try:
        previous_input, history, label_material, label_growth, label_emotion = conn.select(sql_select)[0]
        history = history[-512:]
        
        if Input == previous_input:
            history = conn.select(sql_select[:-1]+'2')[1][1][-512:]
        
        msg = await get_socrates_answer(history)
        history += '\n' + Input
        print('------ History Found ------')
        print(f'Label_Material: {label_material}, Label_Growth: {label_growth}, Label_Emotion: {label_emotion}')
    except (TypeError, IndexError):
        history = Input
        msg = await get_socrates_answer(history)
        print('------ History Not Found ------')
        
    if msg:
        history += '\n' + msg
        if len(history) > 512:
            # 进行关键句提取
            history_sum = await textrank_summarization(history)
            if history_sum:
                history = history_sum
                print('------ History Has Been Summarized ------')
            
        sql_update = f'insert into history(User_ID, Input, Output, Update_Time, History, Label_Material, Label_Growth, Label_Emotion) \
                    values (\'{user_id}\', \'{Input}\', \'{msg}\', \'{date_time}\', \'{history}\', \'{label_scores[0]}\', \'{label_scores[1]}\', \'{label_scores[2]}\');'
        conn.update(sql_update)
            
        try:
            await socrates.send(Message(msg))
            # await socrates.send(Message(history))
            print('------ History Info ------\n', history)
        except CQHttpError:
            await socrates.send(Message('CQHttpError...'))
            
    else:
        await socrates.send(Message('调用文心ERNIE大模型失败...'))
    
    conn.close()


async def get_socrates_answer(text_str):
    MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/text_gen/Socrates_V1"
    request_url = "{}?access_token={}".format(MODEL_API_URL, ACCESS_TOKEN)
    PARAMS = {"max_gen_len": 128}
    PARAMS["text"] = f'问题：{text_str}\t反问：'

    response = requests.post(url=request_url, json=PARAMS)
    response_json = response.json()
    print(response_json)
    try:
        return response_json['result']['content']
    except KeyError:
        return False

async def get_topic_classify(text_str):
    MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/text_cls/Socrates_Classify"
    request_url = "{}?access_token={}".format(MODEL_API_URL, ACCESS_TOKEN)
    PARAMS = {}
    PARAMS["text"] = text_str

    response = requests.post(url=request_url, json=PARAMS)
    response_json = response.json()
    results = response_json['results']
    score = {'物质': -1.0, '成长': -1.0, '情感': -1.0}
    for result in results:
        name = result['name']
        score[name] = result['score']
    return list(score.values())


async def textrank_summarization(doc, len_max=128, ratio=1):
    summ = TextRankSummarization(len_max=len_max, ratio=ratio)
    summ = summ.analysis(doc)
    return summ


