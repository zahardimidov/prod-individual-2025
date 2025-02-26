from aiogram.fsm.state import State, StatesGroup


class CampaignsMenu(StatesGroup):
    START = State()
    DETAIL = State()
    DELETE = State()

    STATS = State()
    DAILY_STATS = State()

    ADVERTISER_STATS = State()
    ADVERTISER_DAILY_STATS = State()

    UPLOAD_IMAGES = State()


class EditCampaign(StatesGroup):
    ad_title = State()
    ad_text = State()

    start_date = State()
    end_date = State()

    gender = State()
    age_from = State()
    age_to = State()
    location = State()

    impressions_limit = State()
    clicks_limit = State()
    cost_per_impression = State()
    cost_per_click = State()

    SAVE = State()
