from infra.database.models import Click, CurrentDate, MLScore, Impression
from infra.database.session import async_session
from infra.repository.advertiser import *
from infra.repository._base import BaseRepository
from infra.repository.campaign import *
from infra.repository.client import *


class CurrentDateRepository(BaseRepository[CurrentDate]):
    model = CurrentDate
    session = async_session


class MLScoreRepository(BaseRepository[MLScore]):
    model = MLScore
    session = async_session


class ImpressionRepository(BaseRepository[Impression]):
    model = Impression
    session = async_session

class ClickRepository(BaseRepository[Click]):
    model = Click
    session = async_session
