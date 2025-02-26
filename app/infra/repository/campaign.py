from infra.database.models import (Advertiser, Campaign, Click, Client,
                                   Impression, MLScore)
from infra.database.session import async_session
from infra.repository._base import BaseRepository
from schemas.ads import RelevantCampaign
from sqlalchemy import and_, func, or_, select


def normalize(S_u, S_min, S_max):
    if S_max == S_min:
        return 1
    N_u = (S_u - S_min) / (S_max - S_min)
    return N_u


class CampaignRepository(BaseRepository[Campaign]):
    model = Campaign
    session = async_session

    async def get_relevant_campaigns(self, client: Client, day: int):
        async with self.session() as session:
            impr_count_subquery = (
                select(func.count(Impression.client_id))
                .where(Impression.campaign_id == Campaign.id)
            ).correlate(Campaign).scalar_subquery()

            seen_subquery = (
                select(func.count(Impression.client_id) > 0)
                .where(Impression.campaign_id == Campaign.id, Impression.client_id == client.id)
            ).correlate(Campaign).scalar_subquery()

            click_count_subquery = (
                select(func.count(Click.client_id))
                .where(Click.campaign_id == Campaign.id)
            ).correlate(Campaign).scalar_subquery()

            clicked_subquery = (
                select(func.count(Click.client_id) > 0)
                .where(Click.campaign_id == Campaign.id, Click.client_id == client.id)
            ).correlate(Campaign).scalar_subquery()

            target_campaigns = select(Campaign.id, Campaign.end_date, Campaign.cost_per_click, Campaign.cost_per_impression, func.coalesce(MLScore.score, 0), seen_subquery, clicked_subquery, click_count_subquery, impr_count_subquery) \
                .outerjoin(Advertiser, Campaign.advertiser_id == Advertiser.id) \
                .outerjoin(MLScore, and_(MLScore.advertiser_id == Advertiser.id, MLScore.client_id == client.id)).where(
                and_(
                    or_(Campaign.location == None,
                        Campaign.location == client.location),
                    or_(Campaign.gender == None, Campaign.gender ==
                        'ALL', Campaign.gender == client.gender),
                    or_(Campaign.age_from == None,
                        Campaign.age_from <= client.age),
                    or_(Campaign.age_to == None, Campaign.age_to >= client.age),
                    and_(Campaign.start_date <= day, Campaign.end_date >= day),
                    and_(impr_count_subquery < func.floor(
                        Campaign.impressions_limit * 1.03))
                )
            )

            target_campaigns = await session.execute(target_campaigns)

            res = target_campaigns.all()

            if not res:
                return

            print(f'After targeting:', len(res))

            max_ml_score = max(res, key=lambda x: x[3])[3]
            min_ml_score = min(res, key=lambda x: x[3])[3]

            mx_possible_profit = 0
            mn_possible_profit = float('inf')

            items: list[RelevantCampaign] = []

            for target in res:
                id, end_date, cost_per_click, cost_per_impression, ml_score, seen, clicked, clicks_count, impr_count = target

                normilized_ml_score = normalize(
                    ml_score, min_ml_score, max_ml_score)
                click_possibility = (1 + clicks_count) / \
                    (2 + impr_count) * normilized_ml_score

                possible_profit = (not seen) * cost_per_impression + \
                    (not clicked) * cost_per_click * click_possibility
                mx_possible_profit = max(mx_possible_profit, possible_profit)
                mn_possible_profit = min(mn_possible_profit, possible_profit)

                item = RelevantCampaign(
                    id=id,
                    cost_per_impression=cost_per_impression,
                    cost_per_click=cost_per_click,
                    clicks_count=clicks_count,
                    impressions_count=impr_count,
                    ml_score=ml_score,
                    normilized_ml_score=normilized_ml_score,
                    click_possibility=click_possibility,
                    possible_profit=possible_profit,
                    clicked=clicked,
                    seen=seen,
                    days_left=end_date-day+1
                )
                items.append(item)

            for item in items:
                item.normilized_possible_profit = normalize(
                    item.possible_profit, mn_possible_profit, mx_possible_profit)
                item.result = (item.normilized_possible_profit *
                               2 + item.normilized_ml_score)

            items = sorted(items, key=lambda x: (x.seen, x.clicked, -x.result))

            print(f'Items:', len(items), f'\n{items=}', '\nbest=', items[0])

            return items

    async def get_relevant_campaign(self, client: Client, day: int):
        results = await self.get_relevant_campaigns(client, day)

        if results:
            return await self.get(id=results[0].id)

    async def stats(self, campaign_id: str):
        async with self.session() as session:
            imprt_stmt = select(func.count(Impression.client_id).label('impressions_count'), func.coalesce(
                func.sum(Impression.cost), 0).label('spent_impressions')).where(Impression.campaign_id == campaign_id)
            clicks_stmt = select(func.count(Click.client_id).label('clicks_count'), func.coalesce(
                func.sum(Click.cost), 0).label('spent_clicks')).where(Click.campaign_id == campaign_id)

            impr: dict = (await session.execute(imprt_stmt)).mappings().one()
            clicks: dict = (await session.execute(clicks_stmt)).mappings().one()

            conversion = round(0 if impr['impressions_count'] ==
                               0 else clicks['clicks_count'] / impr['impressions_count'] * 100)
            spent_total = clicks['spent_clicks'] + impr['spent_impressions']

            return dict(conversion=conversion, spent_total=spent_total, **impr, **clicks)

    async def daily_stats(self, campaign_id: str, date: int):
        async with self.session() as session:
            imprt_stmt = select(func.count(Impression.client_id).label('impressions_count'), func.coalesce(func.sum(
                Impression.cost), 0).label('spent_impressions')).where(Impression.campaign_id == campaign_id, Impression.date == date)
            clicks_stmt = select(func.count(Click.client_id).label('clicks_count'), func.coalesce(func.sum(
                Click.cost), 0).label('spent_clicks')).where(Click.campaign_id == campaign_id, Click.date == date)

            impr: dict = (await session.execute(imprt_stmt)).mappings().one()
            clicks: dict = (await session.execute(clicks_stmt)).mappings().one()

            conversion = round(0 if impr['impressions_count'] ==
                               0 else clicks['clicks_count'] / impr['impressions_count'] * 100)
            spent_total = clicks['spent_clicks'] + impr['spent_impressions']

            return dict(conversion=conversion, spent_total=spent_total, **impr, **clicks)
