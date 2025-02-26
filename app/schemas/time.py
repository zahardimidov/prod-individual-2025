from schemas._base import RequestModel, NonNegativeInt


class TimeAdvanceSchema(RequestModel):
    current_date: NonNegativeInt
