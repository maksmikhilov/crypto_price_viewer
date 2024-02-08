import time
from aiohttp import web
from aiogram import types

from bot_init import bot
import db

routes = web.RouteTableDef()

@routes.get('/chat_gpt/create_db')
async def create_db(request):
    db.create_db()
    return web.Response(text="Hello, world")
    

@routes.post('/chat_gpt/text_alert')
async def text_alert(request):
    alert_data = await request.json()
    text = alert_data['text']

    users_id = ['6197833365', '265593331']
    for user_id in users_id:
        await bot.send_message(user_id, text)
    return web.Response(text="Hello, world")