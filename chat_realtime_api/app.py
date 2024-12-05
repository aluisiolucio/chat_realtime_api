from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chat_realtime_api.api.v1.routers.token import router as token_router
from chat_realtime_api.api.v1.routers.users import router as users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'],
    allow_headers=['*'],
)

app.include_router(users_router)
app.include_router(token_router)


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': '/'}
