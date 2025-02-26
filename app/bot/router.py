from aiogram import F, Router
from aiogram.filters import CommandStart, ExceptionTypeFilter
from aiogram.types import CallbackQuery, ErrorEvent, Message
from aiogram_dialog.api.exceptions import (OutdatedIntent, UnknownIntent,
                                           UnknownState)
from bot.config import keyboards as kb
from bot.config import messages
from bot.dialogs.ai.states import AIStates
from bot.dialogs.auth.states import SetProfile
from bot.dialogs.campaigns.states import CampaignsMenu
from bot.utils import DialogManager, UserMiddleware
from exceptions import ServiceException
from infra import redis
from infra.database.models import Advertiser

router = Router()

router.message.middleware(UserMiddleware())


@router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await message.answer(messages['start'], reply_markup=kb.main)


@router.callback_query(F.data == 'login')
async def login(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(SetProfile.START)


@router.callback_query(F.data == 'logout')
async def logout(callback: CallbackQuery, dialog_manager: DialogManager):
    await redis.delete(key=callback.from_user.id)
    await dialog_manager.start(SetProfile.START)

@router.message(F.text == messages['profile_btn'])
async def profile(message: Message, advertiser: Advertiser):
    await message.answer(
        text=messages['profile'].format(
            advertiser_id=advertiser.id, name=advertiser.name),
        reply_markup=kb.logout
    )


@router.message(F.text == messages['campaigns_btn'])
async def get_my_campaigns(message: Message, advertiser: Advertiser, dialog_manager: DialogManager):
    await dialog_manager.start(CampaignsMenu.START)


@router.message(F.text == messages['ai_btn'])
async def generate_text(message: Message, advertiser: Advertiser, dialog_manager: DialogManager):
    await dialog_manager.start(AIStates.START)


@router.errors(ExceptionTypeFilter(UnknownState, UnknownIntent, OutdatedIntent))
async def handle_states_exception(event: ErrorEvent, dialog_manager: DialogManager):
    update = event.update.message or event.update.callback_query
    user = update.from_user.id

    await update.bot.send_message(chat_id=user, text=messages['start'], reply_markup=kb.main)


@router.errors(F.update.message.as_("message"), ExceptionTypeFilter(ServiceException))
async def handle_service_exception(event: ErrorEvent, message: Message):
    exception: ServiceException = event.exception
    await message.answer(text=exception.detail)


@router.error(F.update.message.as_("message"))
async def handle_exception(event: ErrorEvent, message: Message):
    detail = event.exception.__dict__.get('detail')
    if detail:
        return await message.answer(text=detail)
    await message.answer(text=str(event.exception))
