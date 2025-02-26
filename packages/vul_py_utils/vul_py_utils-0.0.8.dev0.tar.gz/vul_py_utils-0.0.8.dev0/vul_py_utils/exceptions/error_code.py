from enum import Enum
from http import HTTPStatus
from ..exceptions.custom import VulcanBaseError


class InternalServerError():
    # Code
    ErrUnknown =            VulcanBaseError(0, "Unknown error", HTTPStatus.INTERNAL_SERVER_ERROR)
    ErrInvalidRequest =     VulcanBaseError(1, "Invalid request", HTTPStatus.BAD_REQUEST)
    ErrFieldCannotBeEmpty = VulcanBaseError(2, "Required field cannot be empty", HTTPStatus.BAD_REQUEST)
    ErrInvalidSignature =   VulcanBaseError(3, "Invalid signature", HTTPStatus.UNAUTHORIZED)
    ErrInvalidJWTToken =    VulcanBaseError(4, "Invalid JWT token", HTTPStatus.UNAUTHORIZED)
    ErrInvalidFACToken =    VulcanBaseError(5, "Invalid Firebase App Check Token", HTTPStatus.BAD_REQUEST)
    ErrTooManyRequests =    VulcanBaseError(6, "Too many requests", HTTPStatus.TOO_MANY_REQUESTS)

