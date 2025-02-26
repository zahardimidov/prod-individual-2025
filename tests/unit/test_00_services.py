import os
import time
from random import choice, randint

import pytest
from app.infra.database.session import run_database
from app.services.advertisers import AdvertiserService
from app.services.campaign import CampaignService
from app.services.client import ClientService
from app.services.time import TimeAdvanceService
from data import advertisers, campaigns, clients
from dotenv import find_dotenv

client_service = ClientService()
campaign_service = CampaignService()
advertiser_service = AdvertiserService()
time_service = TimeAdvanceService()

advertiser_campaigns = {}


start_time = None
def start():
    global start_time
    start_time = time.time()
def finish():
    print(f'{time.time() - start_time}')


async def update_ml_scores(mn, mx):
    mx_score = 0
    mn_score = float('inf')
    for client in clients():
        for advertiser in advertisers():
            score = randint(mn, mx)
            mx_score = max(mx, mx_score)
            mn_score = min(mn, mn_score)
            await advertiser_service.set_ml_score(client_id=client['client_id'], advertiser_id=advertiser['advertiser_id'], score=score)
    print(f'\n{mn_score=}\n{mx_score=}\n')
    

@pytest.mark.asyncio
async def test_create_db():
    db_old_file = find_dotenv('database.db')
    if db_old_file:
        os.remove(db_old_file)
        time.sleep(1)
    await run_database()
    time.sleep(1)


@pytest.mark.asyncio
async def test_create_data():
    await client_service.bulk(clients())
    await advertiser_service.bulk(advertisers())

    for ad in campaigns():
        advertiser_id = choice(advertisers())['advertiser_id']
        if not advertiser_id in advertiser_campaigns:
            advertiser_campaigns[advertiser_id] = []

        campaign_data = ad.copy()
        if campaign_data.get('targeting'):
            target_data = campaign_data.pop('targeting')
            campaign_data.update(target_data)

        campaign = await campaign_service.create_campaign(advertiser_id=advertiser_id, data=campaign_data)
        advertiser_campaigns[advertiser_id].append(campaign.to_dict())

    
    await update_ml_scores(1, 100)

@pytest.mark.asyncio
async def test_get_relevant():
    client = clients()[4]
    client = await client_service.repo.get(client['client_id'])

    await time_service.set_date(12)

    start()
    result = await campaign_service.repo.get_relevant_campaigns(client, 12)
    finish()

    for i in result:
        print(i.model_dump_json(indent=4), '\n\n')






'''
seen, score, clicked
a = [(True, 100, True), (True, 100, False), (True, 50, True), (True, 50, False), (False, 100, False), (False, 50, False)]
sorted(a, key=lambda x: (x[0], x[2], -x[1]))
[(False, 100, False), (False, 50, False), (True, 100, False), (True, 50, False), (True, 100, True), (True, 50, True)]
'''


    
