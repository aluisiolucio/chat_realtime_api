from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'],
    allow_headers=['*'],
)


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': '/'}
