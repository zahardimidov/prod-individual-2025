from fastapi import APIRouter, Depends
from schemas.time import TimeAdvanceSchema
from services.time import TimeAdvanceService

router = APIRouter(prefix='/time', tags=['Time'])


@router.post('/advance', response_model=TimeAdvanceSchema, status_code=200)
async def time_advance(
    data: TimeAdvanceSchema,
    service: TimeAdvanceService = Depends(TimeAdvanceService)
):
    value = await service.set_date(value=data.current_date)

    return dict(current_date=value)
