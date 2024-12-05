from typing import Dict

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from chat_realtime_api.api.v1.errors.error_handlers import handle_error
from chat_realtime_api.api.v1.schemas.token import TokenOutputSchema
from chat_realtime_api.infra.config.security import get_current_user
from chat_realtime_api.infra.db.session import get_session
from chat_realtime_api.infra.sqlalchemy_repositories.users import (
    SqlAlchemyUserRepository,
)
from chat_realtime_api.services.token import RefreshToken, Token, TokenInput

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])


@router.post('/login', response_model=TokenOutputSchema)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    repo = SqlAlchemyUserRepository(session)
    service = Token(repo)

    try:
        token = service.execute(
            TokenInput(
                username=form_data.username,
                password=form_data.password,
            )
        )

        return TokenOutputSchema(
            id=token.id,
            username=token.username,
            access_token=token.access_token,
            token_type=token.token_type,
        )
    except Exception as e:
        print(e)
        raise handle_error(e)


@router.post('/refresh_token', response_model=TokenOutputSchema)
def refresh_access_token(
    current_user: Dict = Depends(get_current_user),
):
    use_case = RefreshToken()
    refresh_token = use_case.execute(
        id=current_user['uid'],
        username=current_user['username'],
    )

    return TokenOutputSchema(
        id=refresh_token.id,
        username=refresh_token.username,
        access_token=refresh_token.access_token,
        token_type=refresh_token.token_type,
    )
