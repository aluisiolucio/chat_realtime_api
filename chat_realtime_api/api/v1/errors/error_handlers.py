from fastapi import HTTPException

from chat_realtime_api.services.errors.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


def handle_error(exception: Exception) -> HTTPException:
    exception_map = {
        UserNotFoundException: (404, 'UserNotFound'),
        UserAlreadyExistsException: (409, 'UserAlreadyExists'),
        InvalidCredentialsException: (401, 'InvalidCredentials'),
    }

    for exc_type, (status_code, error) in exception_map.items():
        if isinstance(exception, exc_type):
            return HTTPException(
                status_code=status_code,
                detail={
                    'error': error,
                    'message': exception.message,
                },
            )

    return HTTPException(
        status_code=500,
        detail={
            'error': 'InternalServerError',
            'message': 'Oops! An unexpected error occurred.',
        },
    )
