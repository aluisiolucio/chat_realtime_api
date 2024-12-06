from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from chat_realtime_api.api.v1.errors.error_handlers import handle_error
from chat_realtime_api.api.v1.schemas.users import (
    UserInputSchema,
    UserOutputSchema,
)
from chat_realtime_api.infra.db.session import get_session
from chat_realtime_api.infra.sqlalchemy_repositories.users import (
    SqlAlchemyUserRepository,
)
from chat_realtime_api.services.users.create import (
    CreateUserInput,
    CreateUserService,
)

router = APIRouter(prefix='/api/v1', tags=['users'])


@router.post(
    '/users',
    status_code=HTTPStatus.CREATED,
    response_model=UserOutputSchema,
)
def create_user(
    user_schema: UserInputSchema,
    session: Session = Depends(get_session),
):
    repo = SqlAlchemyUserRepository(session)
    service = CreateUserService(repo)
    try:
        user = service.execute(
            CreateUserInput(
                name=user_schema.name,
                username=user_schema.username,
                password=user_schema.password,
            )
        )

        return UserOutputSchema(
            id=user.id,
            name=user.name,
            username=user.username,
        )
    except Exception as e:
        print(e)
        raise handle_error(e)
