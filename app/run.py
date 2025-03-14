from api import router
from bot import process_update, run_bot_webhook
from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, Response
from infra import redis, settings
from infra.database.session import run_database
from infra.s3.storage import Storage
from prometheus_fastapi_instrumentator import Instrumentator


async def on_startup(app: FastAPI):
    await redis.flush()
    await run_database()
    await redis.set('moderation', 0)

    print(settings.TEST_MODE)

    if not settings.TEST_MODE:
        await run_bot_webhook()
    yield

app = FastAPI(lifespan=on_startup)
app.add_api_route('/webhook', endpoint=process_update, methods=['post'], include_in_schema=False)
app.include_router(router)

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


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/images/{filename}", include_in_schema=False)
async def images(filename):
    storage = Storage('images')
    if not await storage.exists(filename):
        raise HTTPException(status_code=404, detail='Картинка не найдена')
    
    headers = {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0"
    }

    content = await storage.read_file(filename)
    return Response(content, media_type="image/png", headers=headers)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = exc._errors[0].get('ctx', {}).get('error') or 'Ошибка в данных запроса'
    return JSONResponse(status_code=400, content=jsonable_encoder({"status": 'error', "message": str(message)}))


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder({"status": 'error', "message": exc.detail}))


@app.exception_handler(Exception)
async def any_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=404, content=jsonable_encoder({"status": 'error', "message": 'Контент не найден'}))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, forwarded_allow_ips='*')
