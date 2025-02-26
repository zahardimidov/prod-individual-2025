from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, ShowMode, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Next
from aiogram_dialog.widgets.text import Const, Format
from bot.config import emoji, messages
from bot.dialogs.ai.states import AIStates
from bot.utils import DialogManager
from infra.database.models import Advertiser


async def cancel_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.done()


async def generate_text(text: str, dialog_manager: DialogManager):
    dialog_manager.__dict__.keys()

    if len(text) < 2:
        raise ValueError('Придумай другое название для рекламы')

    advertiser: Advertiser = dialog_manager.middleware_data['advertiser']

    generated_text = await dialog_manager.bot.yandexcloud.generate_text(advertiser_name=advertiser.name, ad_name=text)

    if not generated_text:
        raise ValueError('Что-то пошло не так')

    dialog_manager.dialog_data.update(
        generated_text=generated_text,
        input_text=text
    )

    await dialog_manager.switch_to(AIStates.PREVIEW)


async def process_input_text(message: Message, dialog_manager: DialogManager):
    await message.answer(emoji['sand'] + 'Генерация началась')

    return await generate_text(message.text, dialog_manager)


async def restart(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    text = dialog_manager.dialog_data.get('input_text')

    if not text:
        return

    msg = await callback.message.answer(emoji['sand'] + 'Повторная генерация началась')
    await generate_text(text, dialog_manager)
    try:
        await msg.delete()
    except:
        pass


async def submit(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(AIStates.RESULT)


async def getter(dialog_manager: DialogManager, **kwargs):
    return dialog_manager.dialog_data


dialog = Dialog(
    Window(
        Const(messages['ai_info']),
        Next(Const(emoji['star'] + "Сгенерировать текст")),
        Button(Const(messages['cancel']), id='cancel', on_click=cancel_dialog),
        state=AIStates.START
    ),
    Window(
        Const('Отправьте название для рекламы'),
        TextInput(id="input_text", filter=process_input_text),
        Back(Const(messages['back'])),
        state=AIStates.INPUT
    ),
    Window(
        Const('<b>Текст:</b>'),
        Format('{generated_text}\n'),
        Const('<b>Как вам результат?</b>'),
        Button(Const(emoji['restart'] + 'Попробовать еще раз'),
               on_click=restart, id='regenerate'),
        Button(Const(emoji['success'] + 'Хорошо'),
               on_click=submit, id='submit'),
        state=AIStates.PREVIEW,
        getter=getter
    ),
    Window(
        Format('{generated_text}\n'),
        state=AIStates.RESULT,
        getter=getter
    )
)
