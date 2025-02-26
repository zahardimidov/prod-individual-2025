
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field
from service import ModerationService

app = FastAPI(title='Модерация текста')
service = ModerationService()

Instrumentator().instrument(app).expose(app, include_in_schema=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        '*'
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InputData(BaseModel):
    text: str = Field(..., min_length=3)


class OutputData(BaseModel):
    toxicity: float


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.post('/validate')
async def validate_text(data: InputData):
    start_date = time.time()
    toxic_propabality = service.validate(data.text)
    print(f'Probability of toxicity: {toxic_propabality:.2f}')
    print(time.time() - start_date)

    return dict(
        toxicity=f'{toxic_propabality:.2f}'
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=4000)
