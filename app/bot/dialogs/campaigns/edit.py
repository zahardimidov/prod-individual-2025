
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Next, Row
from aiogram_dialog.widgets.text import Const, Format
from bot.config import emoji, messages
from bot.dialogs.campaigns.states import EditCampaign, CampaignsMenu
from infra.database.models import Advertiser
from schemas.campaign import CampaignRequest
from bot.utils import DialogManager


async def process_ad_title(message: Message, dialog_manager: DialogManager):
    ad_title = CampaignRequest.fields.ad_title.validate(
        message.text, strict=False)

    if ad_title is None:
        return
    
    await dialog_manager.bot.moderation.validate_text(ad_title, strict=True)
    dialog_manager.dialog_data.update(ad_title=ad_title)

    await dialog_manager.next()


async def process_ad_text(message: Message, dialog_manager: DialogManager):
    ad_text = CampaignRequest.fields.ad_text.validate(
        message.text, strict=False)

    if ad_text is None:
        return
    
    await dialog_manager.bot.moderation.validate_text(ad_text, strict=True)
    dialog_manager.dialog_data.update(ad_text=ad_text)

    await dialog_manager.next()


async def process_start_date(message: Message, dialog_manager: DialogManager):
    start_date = CampaignRequest.fields.start_date.validate(
        message.text, strict=False)

    if start_date is None:
        return

    await dialog_manager.bot.campaigns.validate_campaign_dates(data=dict(
        start_date=start_date
    ))
    dialog_manager.dialog_data.update(start_date=start_date)

    await dialog_manager.next()


async def process_end_date(message: Message, dialog_manager: DialogManager):
    end_date = CampaignRequest.fields.end_date.validate(
        message.text, strict=False)

    if end_date is None:
        return

    start_date = dialog_manager.dialog_data['start_date']

    await dialog_manager.bot.campaigns.validate_campaign_dates(data=dict(
        start_date=start_date,
        end_date=end_date
    ))
    dialog_manager.dialog_data.update(end_date=end_date)

    await dialog_manager.next()


async def process_gender(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if '_male' in button.widget_id:
        dialog_manager.dialog_data.update(gender="MALE")
    if '_female' in button.widget_id:
        dialog_manager.dialog_data.update(gender="FEMALE")
    if '_all' in button.widget_id:
        dialog_manager.dialog_data.update(gender="ALL")

    await dialog_manager.next()


async def process_age_from(message: Message, dialog_manager: DialogManager):
    age_from = CampaignRequest.fields.targeting.fields.age_from.validate(
        message.text, strict=False)

    if age_from is None:
        return

    dialog_manager.dialog_data.update(age_from=age_from)

    await dialog_manager.next()


async def process_age_to(message: Message, dialog_manager: DialogManager):
    age_to = CampaignRequest.fields.targeting.fields.age_to.validate(
        message.text, strict=False)

    if age_to is None:
        return

    age_from = dialog_manager.dialog_data['age_from']

    if age_to < age_from:
        raise ValueError(
            'Минимальный возраст для показа не может превышать максимальный')

    dialog_manager.dialog_data.update(age_to=age_to)

    await dialog_manager.next()


async def process_location(message: Message, dialog_manager: DialogManager):
    location = CampaignRequest.fields.targeting.fields.location.validate(
        message.text, strict=False)

    if location is None:
        return

    dialog_manager.dialog_data.update(location=location)

    await dialog_manager.next()


async def process_impressions_limit(message: Message, dialog_manager: DialogManager):
    impressions_limit = CampaignRequest.fields.impressions_limit.validate(
        message.text, strict=False)

    if impressions_limit is None:
        return

    dialog_manager.dialog_data.update(impressions_limit=impressions_limit)

    await dialog_manager.next()


async def process_clicks_limit(message: Message, dialog_manager: DialogManager):
    clicks_limit = CampaignRequest.fields.clicks_limit.validate(
        message.text, strict=False)

    if clicks_limit is None:
        return

    impressions_limit = dialog_manager.dialog_data['impressions_limit']

    if impressions_limit < clicks_limit:
        raise ValueError(
            'Количество переходов не может превышать количество показов')

    dialog_manager.dialog_data.update(clicks_limit=clicks_limit)

    await dialog_manager.next()


async def process_cost_per_impression(message: Message, dialog_manager: DialogManager):
    cost_per_impression = CampaignRequest.fields.cost_per_impression.validate(
        message.text, strict=False)

    if cost_per_impression is None:
        return

    dialog_manager.dialog_data.update(cost_per_impression=cost_per_impression)

    await dialog_manager.next()


async def process_cost_per_click(message: Message, dialog_manager: DialogManager):
    cost_per_click = CampaignRequest.fields.cost_per_click.validate(
        message.text, strict=False)

    if cost_per_click is None:
        return

    dialog_manager.dialog_data.update(cost_per_click=cost_per_click)

    await dialog_manager.next()


async def details_getter(dialog_manager: DialogManager, **kwargs):
    return dialog_manager.dialog_data


async def cancel_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.clear()
    await dialog_manager.start(CampaignsMenu.START)


async def save_campaign(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    advertiser: Advertiser = dialog_manager.middleware_data.get('advertiser')

    campaign_id = dialog_manager.dialog_data.pop('campaign_id') if dialog_manager.dialog_data.get('campaign_id') else None

    data = dialog_manager.bot.campaigns.parse_request_data(dialog_manager.dialog_data)

    print(advertiser.id, campaign_id, data)

    if campaign_id:
        await dialog_manager.bot.campaigns.update_campaign(campaign_id=campaign_id, data=data)

    try:
        await dialog_manager.bot.campaigns.create_campaign(advertiser.id, data)
    except Exception as e:
        print(e)
    await dialog_manager.start(CampaignsMenu.START)


def editing(data: dict, widget: Whenable, dialog_manager: DialogManager):
    if dialog_manager.start_data and not dialog_manager.dialog_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
    return 'campaign_id' in dialog_manager.dialog_data


back_btn = Back(text=Const(emoji['back'] + 'Назад'))
continue_btn = Next(text=Const("Пропустить изменение"), when=editing)

dialog = Dialog(
    Window(
        Const("Название рекламы:"),
        TextInput(
            id="ad_title",
            filter=process_ad_title
        ),
        continue_btn,
        Button(Const("Отменить"), on_click=cancel_dialog, id="cancel_editing"),
        state=EditCampaign.ad_title
    ),
    Window(
        Const("Текст рекламы:"),
        TextInput(
            id="ad_text",
            filter=process_ad_text
        ),
        continue_btn,
        back_btn,
        state=EditCampaign.ad_text
    ),
    Window(
        Const("Дата начала рекламы:"),
        TextInput(
            id="start_date",
            filter=process_start_date
        ),
        continue_btn,
        back_btn,
        state=EditCampaign.start_date
    ),
    Window(
        Const("Дата окончания рекламы:"),
        TextInput(
            id="end_date",
            filter=process_end_date
        ),
        continue_btn,
        back_btn,
        state=EditCampaign.end_date
    ),
    Window(
        Const("Пол аудитории:"),
        Row(
            Button(Const('Мужчины'), id='campaign_gender_male',
                   on_click=process_gender),
            Button(Const('Женщины'), id='campaign_gender_female',
                   on_click=process_gender)
        ),
        Button(Const('Все'), id='campaign_gender_all',
               on_click=process_gender),
        continue_btn,
        back_btn,
        state=EditCampaign.gender
    ),
    Window(
        Const("Минимальный возраст аудитории:"),
        TextInput(
            id="age_from",
            filter=process_age_from
        ),
        continue_btn,
        back_btn,
        state=EditCampaign.age_from
    ),
    Window(
        Const("Максимальный возраст аудитории:"),
        TextInput(
            id="age_to",
            filter=process_age_to
        ),
        continue_btn,
        back_btn,
        state=EditCampaign.age_to
    ),
    Window(
        Const("Локация аудитории:"),
        TextInput(
            id="location",
            filter=process_location
        ),
        continue_btn,
        back_btn,
        state=EditCampaign.location
    ),
    Window(
        Const("Лимит показов для рекламного объявления:"),
        TextInput(
            id="impressions_limit",
            filter=process_impressions_limit
        ),
        continue_btn,
        back_btn,
        state=EditCampaign.impressions_limit
    ),
    Window(
        Const("Лимит переходов для рекламного объявления:"),
        TextInput(
            id="clicks_limit",
            filter=process_clicks_limit
        ),
        continue_btn,
        back_btn,
        state=EditCampaign.clicks_limit
    ),
    Window(
        Const("Стоимость одного показа объявления:"),
        TextInput(
            id="cost_per_impression",
            filter=process_cost_per_impression
        ),
        continue_btn,
        back_btn,
        state=EditCampaign.cost_per_impression
    ),
    Window(
        Const("Стоимость одного перехода (клика) по объявлению:"),
        TextInput(
            id="cost_per_click",
            filter=process_cost_per_click
        ),
        continue_btn,
        back_btn,
        state=EditCampaign.cost_per_click
    ),
    Window(
        Const('<b>Результат</b>\n'),
        Format(messages['campaign_base_info']),
        Format(messages['details']),
        Button(Const("Сохранить"), on_click=save_campaign, id='save_campaign'),
        back_btn,
        state=EditCampaign.SAVE,
        getter=details_getter
    )
)
