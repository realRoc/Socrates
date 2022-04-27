# from nonebot.adapters.cqhttp import Message
# from nonebot import on_command
# from nonebot.plugin import on_message
# from nonebot.rule import to_me
# from nonebot.typing import T_State
# from nonebot.adapters import Bot, Event
# import requests
# from aiocqhttp.exceptions import Error as CQHttpError
# from nonebot.adapters.cqhttp.message import MessageSegment
# import httpx
# from nonebot.log import logger
# import json


# socrates = on_message(rule=to_me(), priority=1)
# @socrates.handle()
# async def handle_receive(bot: Bot, event: Event, state: T_State):
#     args = str(event.get_message()).strip()
#     if args:
#         state['input'] = args


# @socrates.got('input', prompt='你想询问我什么问题呢？')
# async def handle_input(bot: Bot, event: Event, state: T_State):
#     input = state['input']
#     msg = await get_socrates_answer(input)
#     try:
#         await socrates.send(Message(msg))
#     except CQHttpError:
#         pass


# async def get_socrates_answer(text_str):
#     MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/text_gen/Socrates_V1"
#     ACCESS_TOKEN = "24.cbb33bc9567d930dfa6bfdbf181de695.2592000.1641788166.282335-25309873"
#     API_KEY = "qsxagODihhOhGs7Rd2zx9KOm"
#     SECRET_KEY = "UF36c5Pp3FSytrhdkc3fYr5Yl1m3dnyj"
#     request_url = "{}?access_token={}".format(MODEL_API_URL, ACCESS_TOKEN)
#     PARAMS = {"max_gen_len": 128}
#     PARAMS["text"] = f'问题：{text_str}\t反问：'
#     response = requests.post(url=request_url, json=PARAMS)
#     response_json = response.json()
#     response_str = json.dumps(response_json, indent=4, ensure_ascii=False)
#     return response_json['result']['content']
