import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('ROOT_PATH'))

import logging

from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from handlers import menu_router
from routes import routes

from bot_init import bot, dp

main_server = os.getenv('MAIN_SERVER')

async def on_startup(dispatcher):
    
    await bot.set_webhook(f'{main_server}/price_viewer', secret_token='secret')

async def on_shutdown(dispatcher):
    await bot.delete_webhook()

def main():
    #logging.basicConfig(level=logging.DEBUG)
    dp.include_router(menu_router)
    
    dp.startup.register(on_startup)
    app = web.Application()
    app.add_routes(routes)
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token='secret',
    )
    webhook_requests_handler.register(app, path='/price_viewer')
    setup_application(app, dp, bot=bot)
    web.run_app(app, host='127.0.0.1', port=6000)


if __name__ == "__main__":
    main()
    