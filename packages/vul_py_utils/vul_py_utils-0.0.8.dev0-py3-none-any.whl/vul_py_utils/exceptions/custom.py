from typing import Union


class VulcanBaseError(Exception):
    code: Union[int, str]
    default_message: str
    http_status_code: int
    extra_message: str
    internal_log_message: str

    def __init__(self, code: Union[int, str], grpc_code: int, default_message: str, http_status_code: int):
        self.code = code
        self.grpc_code = grpc_code
        self.default_message = default_message
        self.http_status_code = http_status_code


class VulcanBaseException(VulcanBaseError):
    def __init__(self, extra_detail: str = "", internal_log_message: str = ""):
        self.extra_message = extra_detail
        self.internal_log_message = internal_log_message
