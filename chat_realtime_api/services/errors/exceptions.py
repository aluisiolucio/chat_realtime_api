class BusinessException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(BusinessException):
    def __init__(self, username: str):
        message = f'User {username} was not found.'
        super().__init__(message)


class UserAlreadyExistsException(BusinessException):
    def __init__(self, username: str):
        message = f'User with username {username} already exists.'
        super().__init__(message)


class RoomAlreadyExistsException(BusinessException):
    def __init__(self, name: str):
        message = f'Room with name {name} already exists.'
        super().__init__(message)


class RoomNotFoundException(BusinessException):
    def __init__(self, room_id: str):
        message = f'Room with id {room_id} was not found.'
        super().__init__(message)


class InvalidCredentialsException(BusinessException):
    def __init__(self):
        message = 'Incorrect email or password'
        super().__init__(message)
