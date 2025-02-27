from typing import Tuple, Union

from fastapi import Request
from fastapi.responses import JSONResponse

from ..exceptions.custom import VulcanBaseError, VulcanBaseException
from ..response2client import to_json_error_response, to_common_error_response


def map_internal_server_error_to_exception(exception: VulcanBaseError) -> Tuple[Union[int, str], str, int]:
    """ First, function will look up at the defined error_map in InternalServerError class
    Then, it will return the code, default_message, and http_status_code of the exception

    Args:
        exception (VulcanBaseError): a VulcanBaseError object in InternalServerError class

    Returns:
        Tuple[int, str, int]: code, default_message, and http_status_code of the exception
    """
    return exception.code, exception.default_message, exception.http_status_code


def map_error2exception(exception: VulcanBaseError) -> Tuple[int, Union[int, str], str, int]:
    """ First, function will look up at the defined error_map in InternalServerError class
    Then, it will return the code, default_message, and http_status_code of the exception

    Args:
        exception (VulcanBaseError): a VulcanBaseError object in InternalServerError class

    Returns:
        Tuple[int, str, str, int]: gRPC Code, ErrorCode, default_message, and http_status_code of the exception
    """
    return exception.grpc_code, exception.code, exception.default_message, exception.http_status_code


def handle_vulcan_exception(request: Request, exception: VulcanBaseException) -> JSONResponse:
    """ This middleware handler will handle the VulcanBaseException and return a JSONResponse

    Args:
        exception (VulcanBaseException): _description_

    Returns:
        JSONResponse: _description_
    """
    return to_json_error_response(exception)


def handle_common_error(request: Request, exception: VulcanBaseException) -> JSONResponse:
    """ This middleware handler will handle the VulcanBaseException and return a JSONResponse
    Following this docs: https://vulcanlabs.atlassian.net/wiki/spaces/Develop/pages/404324461/Defined+Error+Codes

    Args:
        exception (VulcanBaseException): _description_

    Returns:
        JSONResponse: _description_
    """
    return to_common_error_response(exception)
