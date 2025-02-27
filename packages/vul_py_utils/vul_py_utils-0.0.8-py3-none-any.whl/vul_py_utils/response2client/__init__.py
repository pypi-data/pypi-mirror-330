"""
    The module contains functions to convert data to JSONResponse
    Beside basic data, it also contains internal error message and error code
    The format of Vulcan response is:
        {
            "data": dict,
            "error": {
                "message": str,
                "code": int
            }
        }
"""

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..exceptions.custom import VulcanBaseException


def to_json_response(data: object, status_code: int = status.HTTP_200_OK) -> JSONResponse:
    """return JSONResponse with data and status code
    
    Args:
        - data[dict]: data to be returned to client
        - status_code[int]: status code of the response, default is 200
    Returns:
        JSONResponse
    """
    return JSONResponse(status_code=status_code,
                        content=jsonable_encoder({"data": data,
                                                  "error": None
                                                  }))


def to_json_error_response(exc: VulcanBaseException) -> JSONResponse:
    """return JSONResponse with error message and error code
    
    Args:
        - exc[Exception]: exception
    Returns:
        JSONResponse
    """
    if exc.extra_message == "":
        error_msg = exc.default_message
    else:
        error_msg = exc.default_message + ": " + exc.extra_message
    return JSONResponse(status_code=exc.http_status_code,
                        content=jsonable_encoder({"data": None,
                                                  "error": {"message": error_msg,
                                                            "code": exc.code}
                                                  }))


def to_common_error_response(exc: VulcanBaseException) -> JSONResponse:
    """return JSONResponse with error message and error code defined in docs:
    https://vulcanlabs.atlassian.net/wiki/spaces/Develop/pages/404324461/Defined+Error+Codes

    Args:
        - exc[Exception]: exception
    Returns:
        JSONResponse
    """
    if exc.extra_message == "":
        error_msg = exc.default_message
    else:
        error_msg = exc.default_message + ": " + exc.extra_message
    return JSONResponse(status_code=exc.http_status_code,
                        content=jsonable_encoder({
                            "message": error_msg,
                            "code": exc.grpc_code,
                            "reason": exc.code,
                        }))


def to_healthcheck_response(status: str, message: str, status_code=status.HTTP_200_OK) -> JSONResponse:
    """return JSONResponse with healthcheck status and message

    Args:
        status (str): _description_
        message (str): _description_
        status_code (_type_, optional): _description_. Defaults to status.HTTP_200_OK.

    Returns:
        JSONResponse: _description_
    """
    return JSONResponse(status_code=status_code,
                        content=jsonable_encoder({"status": status,
                                                  "message": message})
                        )


def to_gpu_healthcheck_dict(status, message, is_cuda_available: bool, gpu_count: int, ) -> dict:
    """return dict with healthcheck status and message

    Args:
        status (_type_): _description_
        message (_type_): _description_
        is_cuda_available (bool): _description_
        gpu_count (int): _description_

    Returns:
        dict: _description_
    """
    return {"status": status,
            "message": message,
            "is_cuda_available": is_cuda_available,
            "gpu_count": gpu_count,
            }
