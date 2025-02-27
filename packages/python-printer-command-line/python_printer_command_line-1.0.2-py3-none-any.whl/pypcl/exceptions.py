#  -*- coding: utf-8 -*-
"""PythonPCL Exceptions classes

Result/Exit codes:

    - `0`  = success
    - `90` = USB device not found :py:exc:`~python-pcl.exceptions.USBNotFoundError`

:author: `Oskar Jaskólski <oskarrro90@gmail.com>`
:copyright: Copyright 2024 Oskar Jaskólski <oskarrro90@gmail.com>
:license: MIT
"""


class Error(Exception):
    """Base class for PythonPCL errors"""

    def __init__(self, msg, status=None):
        super().__init__(self)
        self.msg = msg
        self.resultcode = 1
        if status is not None:
            self.resultcode = status

    def __str__(self):
        return self.msg


class USBNotFoundError(Error):
    """Device wasn't found (probably not plugged in)

    The USB device seems to be not plugged in.
    Ths returncode for this exception is `90`.
    """

    def __init__(self, msg=""):
        super().__init__(self, msg)
        self.msg = msg
        self.resultcode = 90

    def __str__(self):
        return f"USB device not found ({self.msg})"
