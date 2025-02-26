
import operator
from io import BytesIO

from aiogram.types import CallbackQuery, ContentType, Message
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (Back, Button, CurrentPage, FirstPage,
                                        LastPage, NextPage, PrevPage, Row,
                                        ScrollingGroup, Select, SwitchTo)
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.media.scroll import MediaScroll
from aiogram_dialog.widgets.text import Const, Format, List, Multi
from bot.config import emoji, messages
from bot.dialogs.campaigns.states import CampaignsMenu, EditCampaign
from infra.database.models import Advertiser
from bot.utils import DialogManager


async def campaigns_getter(dialog_manager: DialogManager, advertiser: Advertiser, **kwargs):
    campaigns_list = await dialog_manager.bot.campaigns.repo.find(advertiser_id=advertiser.id)
    campaigns_data = [(campaign.ad_title, campaign.id)
                      for campaign in campaigns_list]

    return dict(
        campaigns=campaigns_data
    )


async def campaign_getter(dialog_manager: DialogManager, advertiser: Advertiser, **kwargs):
    campaign_id = dialog_manager.dialog_data['campaign_id']
    campaign = await dialog_manager.bot.campaigns.get_campaign(campaign_id=campaign_id, advertiser_id=advertiser.id)

    if not campaign:
        return dialog_manager.done()
    
    dialog_manager.dialog_data.update(**campaign.to_dict(), images=campaign.images)

    return dialog_manager.dialog_data


async def detail_view(callback: CallbackQuery, select: Select, dialog_manager: DialogManager, campaign_id: str, **kwargs):
    dialog_manager.dialog_data.update(campaign_id=campaign_id)
    await dialog_manager.switch_to(CampaignsMenu.DETAIL)


async def campaign_stats_getter(dialog_manager: DialogManager, **kwargs):
    campaign_id = dialog_manager.dialog_data['campaign_id']

    data = await dialog_manager.bot.stats.get_campaign_stats(campaign_id=campaign_id)
    dialog_manager.dialog_data.update(**data)

    return dialog_manager.dialog_data


async def campaign_daily_stats_getter(dialog_manager: DialogManager, **kwargs):
    campaign_id = dialog_manager.dialog_data['campaign_id']

    days = await dialog_manager.bot.stats.get_campaign_daily_stats(campaign_id=campaign_id)
    dialog_manager.dialog_data.update(days=days)

    return dialog_manager.dialog_data


async def advertiser_stats_getter(dialog_manager: DialogManager, advertiser: Advertiser, **kwargs):
    return await dialog_manager.bot.stats.get_advertiser_stats(advertiser.id)


async def advertiser_daily_stats_getter(dialog_manager: DialogManager, advertiser: Advertiser, **kwargs):
    days = await dialog_manager.bot.stats.get_advertiser_daily_stats(advertiser.id)
    return dict(days=days)


async def create_new_campaign(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(EditCampaign.ad_title)


async def delete_campaign(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    campaign_id = dialog_manager.dialog_data['campaign_id']
    await dialog_manager.bot.campaigns.remove_campaign(campaign_id=campaign_id)
    dialog_manager.dialog_data.clear()
    await dialog_manager.switch_to(CampaignsMenu.START)


async def edit_exist_campaign(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(EditCampaign.ad_title, data=dialog_manager.dialog_data)


async def reset_images(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    campaign_id = dialog_manager.dialog_data['campaign_id']
    await dialog_manager.bot.campaigns.update_campaign_images(campaign_id, images=[])
    await dialog_manager.switch_to(CampaignsMenu.DETAIL)


async def confirm_images(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    campaign_id = dialog_manager.dialog_data['campaign_id']
    uploaded_images = dialog_manager.dialog_data.get('uploaded_images', [])

    if uploaded_images:
        await dialog_manager.bot.campaigns.update_campaign_images(campaign_id, images=uploaded_images)
        dialog_manager.dialog_data['uploaded_images'] = []
    await dialog_manager.switch_to(CampaignsMenu.DETAIL)


async def uploaded_photo_handler(
        message: Message,
        message_input: MessageInput,
        dialog_manager: DialogManager,
):
    file = await message.bot.get_file(message.photo[-1].file_id)

    with BytesIO() as byte_stream:
        await message.bot.download_file(file.file_path, byte_stream)
        file_bytes = byte_stream.read()

    print(f'{file.file_path=}')

    if not dialog_manager.dialog_data.get('uploaded_images'):
        dialog_manager.dialog_data['uploaded_images'] = []

    if len(dialog_manager.dialog_data['uploaded_images']) < 10:
        dialog_manager.dialog_data['uploaded_images'].append(file_bytes)
    else:
        message.answer('Вы можете загрузить до 10 фотографий')


def have_images(data: dict, widget: Whenable, dialog_manager: DialogManager):
    return 'images' in dialog_manager.dialog_data and dialog_manager.dialog_data['images']


def scrolling_images(data: dict, widget: Whenable, dialog_manager: DialogManager):
    return 'images' in dialog_manager.dialog_data and len(dialog_manager.dialog_data['images']) > 1


dialog = Dialog(
    Window(
        Const(emoji["email"] +
              "<b>Все ваши рекламные кампании представлены ниже:</b>"),
        SwitchTo(Const(emoji['stats'] + 'Смотреть статистику'), id='advertiser_stats_btn',
                 state=CampaignsMenu.ADVERTISER_STATS),
        Button(Const(emoji['email'] + 'Создать рекламную кампанию'), id='create_campaign_btn',
               on_click=create_new_campaign),
        ScrollingGroup(
            Select(
                text=Format("{item[0]}"),
                id='s_campaigns',
                item_id_getter=operator.itemgetter(1),
                items='campaigns',
                on_click=detail_view
            ),
            id="campaigns_group",
            width=1,
            height=4
        ),

        state=CampaignsMenu.START,
        getter=campaigns_getter
    ),
    Window(
        MediaScroll(
            StaticMedia(url=Format('{item}')),
            items='images',
            id="images_group",
            when=have_images
        ),

        Format(messages['campaign_base_info']),
        Format(messages['details']),
        Row(
            PrevPage(scroll="images_group"),
            CurrentPage(scroll="images_group", text=Format(
                "Фото {current_page1}/{pages}")),
            NextPage(scroll="images_group"),
            when=scrolling_images
        ),
        SwitchTo(text=Const(emoji['stats'] + 'Статистика'),
                 id='stats_btn', state=CampaignsMenu.STATS),
        SwitchTo(text=Const(emoji['upload'] + 'Загрузить фото'),
                 id='upload_images', state=CampaignsMenu.UPLOAD_IMAGES),
        Button(text=Const(emoji['restart'] + 'Перезаписать'),
               id='rewrite_btn', on_click=edit_exist_campaign),
        SwitchTo(text=Const("Удалить"), id='delete_campaign',
                 state=CampaignsMenu.DELETE),
        Back(text=Const('Назад')),
        state=CampaignsMenu.DETAIL,
        getter=campaign_getter
    ),
    Window(
        Format(messages['campaign_base_info']),
        Format(messages['campaign_stats']),
        SwitchTo(text=Const(emoji['calendar'] + 'По дням'),
                 id='daily_stats_btn', state=CampaignsMenu.DAILY_STATS),
        Back(text=Const('Назад')),
        state=CampaignsMenu.STATS,
        getter=campaign_stats_getter
    ),
    Window(
        Format(messages['campaign_base_info']),
        List(
            Multi(
                Format("<b>День {item[date]}</b>"),
                Format(messages['campaign_stats'].replace(
                    '{', "{item[").replace('}', "]}"))
            ),
            items='days',
            id="daily_stats_group",
            page_size=1
        ),
        Row(
            FirstPage(scroll="daily_stats_group"),
            PrevPage(scroll="daily_stats_group"),
            NextPage(scroll="daily_stats_group"),
            LastPage(scroll="daily_stats_group")
        ),
        Back(text=Const('Назад')),
        state=CampaignsMenu.DAILY_STATS,
        getter=campaign_daily_stats_getter
    ),

    Window(
        Const(emoji['stats'] +
              '<b>Сводная статистика по всем рекламным кампаниям</b>\n'),
        Format(messages['campaign_stats']),
        SwitchTo(text=Const(emoji['calendar'] + 'По дням'), id='advertiser_daily_stats_btn',
                 state=CampaignsMenu.ADVERTISER_DAILY_STATS),
        SwitchTo(text=Const('Назад'), id='advertiser_stats_back_btn',
                 state=CampaignsMenu.START),
        state=CampaignsMenu.ADVERTISER_STATS,
        getter=advertiser_stats_getter
    ),
    Window(
        List(
            Multi(
                Const(
                    emoji['stats'] + '<b>Ежедневная статистика по всем рекламным кампаниям</b>\n'),
                Format("<b>День {item[date]}</b>"),
                Format(messages['campaign_stats'].replace(
                    '{', "{item[").replace('}', "]}"))
            ),
            items='days',
            id="advertiser_daily_stats_group",
            page_size=1
        ),
        Row(
            FirstPage(scroll="advertiser_daily_stats_group"),
            PrevPage(scroll="advertiser_daily_stats_group"),
            NextPage(scroll="advertiser_daily_stats_group"),
            LastPage(scroll="advertiser_daily_stats_group")
        ),
        SwitchTo(text=Const('Назад'), id='advertiser_daily_stats_back_btn',
                 state=CampaignsMenu.START),
        state=CampaignsMenu.ADVERTISER_DAILY_STATS,
        getter=advertiser_daily_stats_getter
    ),
    Window(
        Format(messages['campaign_base_info']),
        Const('Вы уверены что хотите удалить кампанию?'),
        SwitchTo(Const("Отменить"), id='switch_back',
                 state=CampaignsMenu.DETAIL),
        Button(Const("Удалить"), id='delete_campaign_yes',
               on_click=delete_campaign),
        state=CampaignsMenu.DELETE,
        getter=campaign_getter
    ),

    Window(
        Const(emoji['upload'] + 'Загрузите до 10 изображений'),
        MessageInput(uploaded_photo_handler,
                     content_types=[ContentType.PHOTO]),
        Button(Const("Завершить"), id='confirm_images',
               on_click=confirm_images),
        Button(Const("Сбросить текущие изображения"),
               id='reset_images', on_click=reset_images),
        SwitchTo(Const("Отменить"), id='switch_back',
                 state=CampaignsMenu.DETAIL),
        state=CampaignsMenu.UPLOAD_IMAGES
    )
)
