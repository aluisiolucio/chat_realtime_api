from http import HTTPStatus

from fastapi import FastAPI

from chat_realtime_api.api.v1.routers.rooms import router as rooms_router
from chat_realtime_api.api.v1.routers.token import router as token_router
from chat_realtime_api.api.v1.routers.users import router as users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(token_router)
app.include_router(rooms_router)


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': '/'}
