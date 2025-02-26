import logging
import os
from typing import Tuple
import inspect


class Logger(logging.Logger):
    def __init__(self, file_path: str = "tmp.log", stack_level: int = 2):
        # Check if directory exists
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        
        self.__logger = logging.getLogger(file_path)
        self.__logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(filename=file_path, mode="a+t")

        formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        self.__logger.addHandler(file_handler)
        print("Init Logger on path", file_path)
        self.__stack_level = stack_level

    def __get_filename_ane_line(self) -> Tuple[str, int]:
        stack = inspect.stack()
        frame = stack[self.__stack_level]
        line_number = frame.lineno
        filename = frame.filename
        return filename, line_number

    def __get_filename_ane_line_log(self, message: str) -> str:
        stack = inspect.stack()
        frame = stack[self.__stack_level]
        return f"[{frame.filename}:{frame.lineno}] - {message}"

    def log_server_error(self, http_code: int = "", internal_code: int = "", request_body: str = "", *args, **kwargs):
        filename, line_number = self.__get_filename_ane_line()
        error_dict = {"http_code": http_code,
                      "internal_error_code": internal_code,
                      "request_body": request_body,
                      }
        if args:
            for i, arg in enumerate(args):
                error_dict[f"arg_{i}"] = arg
        if kwargs:
            for key, value in kwargs.items():
                error_dict[key] = value
        error_log = f"[{filename}:{line_number}] - {error_dict}"
        self.__logger.error(msg=error_log)

    def log_message(self, message: str):
        log_msg = self.__get_filename_ane_line_log(message)
        self.__logger.info(msg=log_msg)
        
    def log_debug(self, debug: str):
        log_msg = self.__get_filename_ane_line_log(debug)
        self.__logger.debug(msg=log_msg)

    def log_warning(self, warning: str):
        log_msg = self.__get_filename_ane_line_log(warning)
        self.__logger.warning(msg=log_msg)

    def log_error(self, error: str):
        log_msg = self.__get_filename_ane_line_log(error)
        self.__logger.error(msg=log_msg)
        
    def log_exception(self, exception):
        self.__logger.exception(msg=exception, exc_info=True)

    def log_critical(self, critical: str):
        log_msg = self.__get_filename_ane_line_log(critical)
        self.__logger.critical(msg=log_msg)

