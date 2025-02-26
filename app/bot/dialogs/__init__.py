from aiogram_dialog import setup_dialogs as setup
from aiogram import Dispatcher
from bot.dialogs.auth.dialog import dialog as auth_dialog
from bot.dialogs.campaigns.menu import dialog as menu_dialog
from bot.dialogs.campaigns.edit import dialog as edit_dialog
from bot.dialogs.ai.dialog import dialog as ai_dialog
from bot.utils import UserMiddleware, custom_manager_factory
from bot.dialogs.ai.dialog import dialog

menu_dialog.message.middleware(UserMiddleware())
menu_dialog.callback_query.middleware(UserMiddleware())

edit_dialog.callback_query.middleware(UserMiddleware())
edit_dialog.message.middleware(UserMiddleware())

dialog.callback_query.middleware(UserMiddleware())
dialog.message.middleware(UserMiddleware())

dialogs = [
    auth_dialog,
    menu_dialog,
    edit_dialog,
    ai_dialog
]

def setup_dialogs(dp: Dispatcher):
    for dialog in dialogs:
        dp.include_router(dialog)
    setup(dp, dialog_manager_factory=custom_manager_factory)
