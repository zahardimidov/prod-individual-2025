from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram import Bot as AiogramBot
from aiogram import Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message as AiogramMessage
from aiogram.types import Update
from aiogram_dialog import ChatEvent
from aiogram_dialog.api.internal.manager import DialogManagerFactory
from aiogram_dialog.api.protocols import DialogRegistryProtocol
from aiogram_dialog.context.media_storage import MediaIdStorage
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.manager.message_manager import MessageManager
from bot.config import keyboards as kb
from bot.config import messages
from infra import redis
from services import *


class Bot(AiogramBot):
    def __init__(self, token, session=None, **kwargs):
        self.advertisers = AdvertiserService()
        self.clients = ClientService()
        self.stats = StatsService()
        self.campaigns = CampaignService()
        self.yandexcloud = YandexCloudService()
        self.moderation = ModerationService()

        default = DefaultBotProperties(parse_mode=ParseMode.HTML)

        super().__init__(token, session, default, **kwargs)


class Message(AiogramMessage):
    bot: Bot


class DialogManager(ManagerImpl):
    def __init__(self, event, message_manager, media_id_storage, registry, router, data):
        from bot import bot
        self.bot: Bot = bot

        super().__init__(event, message_manager, media_id_storage, registry, router, data)


class CustomManager(DialogManagerFactory):
    def __init__(
            self, **kwargs
    ) -> None:
        self.message_manager = MessageManager()
        self.media_id_storage = MediaIdStorage()

        print(kwargs)

    def __call__(
            self, event: ChatEvent, data: dict,
            registry: DialogRegistryProtocol,
            router: Router,
    ) -> DialogManager:
        manager = DialogManager(
            event=event,
            data=data,
            message_manager=self.message_manager,
            media_id_storage=self.media_id_storage,
            registry=registry,
            router=router
        )

        return manager
    
custom_manager_factory = lambda **kwargs: CustomManager()(**kwargs)


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: dict[str: Any],
    ) -> Any:
        advertiser_id = await redis.get(message.from_user.id)

        if not advertiser_id:
            return await message.answer(messages['login'], reply_markup=kb.login)

        advertiser = await message.bot.advertisers.repo.get(advertiser_id.decode())

        if not advertiser:
            return await message.answer(messages['login'], reply_markup=kb.login)

        data['advertiser'] = advertiser

        return await handler(message, data)
