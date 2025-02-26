from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Next, Row, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from bot.config import emoji
from bot.config import keyboards as kb
from bot.config import messages
from bot.dialogs.auth.states import SetProfile
from bot.utils import DialogManager
from infra import redis


async def process_advertiser_id(message: Message, dialog_manager: DialogManager, **kwargs):
    advertiser_id = message.text.strip().replace('\n', '')

    if len(advertiser_id) > 100:
        raise ValueError(
            "Длина идентификатора не может превышать 100 символов")

    advertiser = await dialog_manager.bot.advertisers.repo.get(advertiser_id)

    dialog_manager.dialog_data.update(advertiser_id=advertiser_id)

    if not advertiser:
        return await dialog_manager.switch_to(SetProfile.CREATE)

    dialog_manager.dialog_data.update(name=advertiser.name)

    return await dialog_manager.switch_to(SetProfile.PREVIEW)


async def process_advertiser_name(message: Message, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.bot.moderation.validate_text(message.text.strip(), strict=True)
    
    dialog_manager.dialog_data.update(name=message.text.strip())
    return await dialog_manager.switch_to(SetProfile.PREVIEW)


async def getter(dialog_manager: DialogManager, **kwargs):
    data = await dialog_manager.load_data()
    return data["dialog_data"] or data["start_data"]


async def finish_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    data = dict(
        name=dialog_manager.dialog_data.get('name'),
        advertiser_id=dialog_manager.dialog_data.get('advertiser_id')
    )
    await dialog_manager.bot.advertisers.bulk([data])
    await redis.set(key=callback.from_user.id, value=dialog_manager.dialog_data['advertiser_id'])
    await dialog_manager.done()
    await callback.message.answer(messages['start'], reply_markup=kb.main)

dialog = Dialog(
    Window(
        Const(emoji['id'] + "<b>Введите ваш идентификатор в системе</b>"),
        TextInput(id="advertiser_id", filter=process_advertiser_id),
        state=SetProfile.START
    ),
    Window(
        Format(
            "Рекламодатель с таким идентификатором не найден " +
            emoji['search'] + ".\n"
            "Создать новый аккаунт с идентификатором <b>{advertiser_id}</b>?"
        ),
        Row(
            Next(Const("Создать"))
        ),
        Row(
            Back(Const(messages['try_again']))
        ),
        state=SetProfile.CREATE,
        getter=getter
    ),
    Window(
        Const(
            "<b>Введите ваше название</b>\n"
        ),
        TextInput(id="name", filter=process_advertiser_name),
        Row(
            SwitchTo(text=Const('Вернуться в начало'),
                     id='try_again', state=SetProfile.START)
        ),
        state=SetProfile.NAME
    ),
    Window(
        Format(messages['profile']),
        Row(
            Button(text=Const('Сохранить'),
                   on_click=finish_dialog, id='save_profile')
        ),
        Row(
            SwitchTo(text=Const(messages['try_again']),
                     id='try_again', state=SetProfile.START)
        ),
        state=SetProfile.PREVIEW,
        getter=getter
    )
)
