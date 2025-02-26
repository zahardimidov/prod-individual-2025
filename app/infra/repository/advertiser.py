from exceptions import SQLException
from infra.database.models import Advertiser, Campaign, Click, Impression
from infra.database.session import async_session
from infra.repository._base import BaseRepository
from sqlalchemy import and_, func, insert, select, update
from sqlalchemy.exc import IntegrityError


class AdvertiserRepository(BaseRepository[Advertiser]):
    model = Advertiser
    session = async_session

    async def bulk_advertisers(self, advertisers: list[dict]):
        ids = []

        async with self.session() as session:
            try:
                async with session.begin():
                    for advertiser_data in advertisers:
                        advertiser_id = advertiser_data.pop('advertiser_id')
                        ids.append(advertiser_id)

                        client = await session.scalar(select(self.model).where(self.model.id == advertiser_id))
                        if client is None:
                            await session.execute(insert(self.model).values(id=advertiser_id, **advertiser_data))
                        else:
                            await session.execute(update(self.model).where(self.model.id == advertiser_id).values(**advertiser_data))
                await session.commit()
            except IntegrityError as e:
                await session.rollback()

                raise SQLException

        async with self.session() as session:
            items = await session.scalars(select(self.model).where(self.model.id.in_(ids)))
            sorted_items = sorted(
                items.all(), key=lambda item: ids.index(item.id))

            return sorted_items

    async def stats(self, advertiser_id: str):
        async with self.session() as session:
            imprt_stmt = select(func.count(Impression.client_id).label('impressions_count'), func.coalesce(func.sum(
                Impression.cost), 0).label('spent_impressions')).join(Campaign).where(Campaign.advertiser_id == advertiser_id)
            clicks_stmt = select(func.count(Click.client_id).label('clicks_count'), func.coalesce(func.sum(
                Click.cost), 0).label('spent_clicks')).join(Campaign).where(Campaign.advertiser_id == advertiser_id)

            impr: dict = (await session.execute(imprt_stmt)).mappings().one()
            clicks: dict = (await session.execute(clicks_stmt)).mappings().one()

            conversion = round(0 if impr['impressions_count'] ==
                               0 else clicks['clicks_count'] / impr['impressions_count'] * 100)
            spent_total = clicks['spent_clicks'] + impr['spent_impressions']

            return dict(conversion=conversion, spent_total=spent_total, **impr, **clicks)

    async def daily_stats(self, advertiser_id: str, date: int):
        async with self.session() as session:
            imprt_stmt = select(func.count(Impression.client_id).label('impressions_count'), func.coalesce(func.sum(Impression.cost), 0).label(
                'spent_impressions')).join(Campaign).where(Campaign.advertiser_id == advertiser_id, Impression.date == date)
            clicks_stmt = select(func.count(Click.client_id).label('clicks_count'), func.coalesce(func.sum(Click.cost), 0).label(
                'spent_clicks')).join(Campaign).where(Campaign.advertiser_id == advertiser_id, Click.date == date)

            impr: dict = (await session.execute(imprt_stmt)).mappings().one()
            clicks: dict = (await session.execute(clicks_stmt)).mappings().one()

            conversion = round(0 if impr['impressions_count'] ==
                               0 else clicks['clicks_count'] / impr['impressions_count'] * 100)
            spent_total = clicks['spent_clicks'] + impr['spent_impressions']

            return dict(conversion=conversion, spent_total=spent_total, **impr, **clicks)
