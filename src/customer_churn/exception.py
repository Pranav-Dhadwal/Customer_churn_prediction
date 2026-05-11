import sys


class CustomException(Exception):
    def __init__(self, error, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()

        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        self.message = (
            "\n" + "=" * 60 + "\n"
            "CUSTOM EXCEPTION\n"
            f"File : {file_name}\n"
            f"Line : {line_number}\n"
            f"Error: {str(error)}\n"
            + "=" * 60
        )

        super().__init__(self.message)

        # suppress original chained traceback
        self.__cause__ = None
        self.__context__ = None
        self.__suppress_context__ = True

    def __str__(self):
        return self.message