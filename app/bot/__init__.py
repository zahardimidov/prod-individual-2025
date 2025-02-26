from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from bot.config import BOT_TOKEN, WEBHOOK_URL
from bot.dialogs import setup_dialogs
from bot.router import router
from fastapi import Request
from bot.utils import Bot


async def run_bot_webhook():
    me = await bot.get_me()
    print(me.username)

    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True, allowed_updates=["message", "edited_channel_post", "callback_query"])

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

dp.include_router(router)

setup_dialogs(dp)


async def process_update(request: Request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)

