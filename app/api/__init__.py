from api.routes.ads import router as ads_router
from api.routes.advertisers import router as advertisers_router
from api.routes.campaign import router as campaign_router
from api.routes.client import router as client_router
from api.routes.stats import router as stats_router
from api.routes.time import router as time_router
from api.routes.features import router as features_router
from fastapi import APIRouter
from fastapi.routing import APIRoute

router = APIRouter(prefix='')

@router.get("/ping", status_code=200, include_in_schema=False)
def ping():
    return {"status": "ok"}

router.include_router(client_router)
router.include_router(advertisers_router)
router.include_router(campaign_router)
router.include_router(ads_router)
router.include_router(stats_router)
router.include_router(time_router)
router.include_router(features_router)

for route in router.routes:
    if isinstance(route, APIRoute):
        route.response_model_exclude_none = True
        parts = route.name.split('_')
        route.operation_id = ''.join(map(str.capitalize, parts))
