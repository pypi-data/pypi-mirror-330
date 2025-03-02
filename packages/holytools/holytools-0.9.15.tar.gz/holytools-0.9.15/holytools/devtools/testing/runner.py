import ctypes
import linecache
import multiprocessing
import os
import threading
import time
import tracemalloc
import unittest
import unittest.mock
import warnings
from abc import abstractmethod
from logging import Logger
from multiprocessing import Process, Value
from unittest import TestSuite

from .result import SuiteRunResult


# ----------------------------------------------


class Runner(unittest.TextTestRunner):
    def __init__(self, logger : Logger, test_name : str, is_manual : bool = False):
        super().__init__(resultclass=None)
        self.logger : Logger = logger
        self.manual_mode : bool = is_manual
        self.test_name : str = test_name

    def run(self, testsuite : TestSuite, tracemalloc_depth : int = 0) -> SuiteRunResult:
        if tracemalloc_depth > 0:
            tracemalloc.start(tracemalloc_depth)

        with warnings.catch_warnings(record=True) as captured_warnings:
            warnings.simplefilter("ignore")
            warnings.simplefilter("always", ResourceWarning)

            result = SuiteRunResult(logger=self.logger,
                                    testsuite_name=self.test_name,
                                    stream=self.stream,
                                    descriptions=self.descriptions,
                                    verbosity=2,
                                    manual_mode=self.manual_mode)
            testsuite(result)
            result.printErrors()

        for warning in captured_warnings:
            if tracemalloc_depth > 0:
                print(f'- Unclosed resources:')
                print(Runner.warning_to_str(warning_msg=warning))
            else:
                self.logger.warning(msg=f'[Warning]: Unclosed resource: \"{warning.message}\."'
                                        f'Enable trace_resourcewarning to obtain object trace')

        warnings.simplefilter("ignore", ResourceWarning)
        if tracemalloc_depth > 0:
            tracemalloc.stop()

        return result

    @staticmethod
    def warning_to_str(warning_msg: warnings.WarningMessage) -> str:
        tb = tracemalloc.get_object_traceback(warning_msg.source)
        frames = list(tb)
        frames = [f for f in frames if Runner.is_relevant(frame=f)]

        result = ''
        for frame in frames:
            file_path = frame.filename
            line_number = frame.lineno
            result += (f'File "{file_path}", line {line_number}\n'
                      f'    {linecache.getline(file_path, line_number).strip()}\n')
        return result

    @staticmethod
    def is_relevant(frame):
        not_unittest = not os.path.dirname(unittest.__file__) in frame.filename
        not_custom_unittest = not os.path.dirname(__file__) in frame.filename
        return not_unittest and not_custom_unittest


class BlockedTester:
    def __init__(self):
        self.shared_bool = Value(ctypes.c_bool, False)

    def check_ok(self, case : str, delay : float) -> bool:
        def do_run():
            threading.Thread(target=self.blocked).start()
            time.sleep(delay)
            check_thread = threading.Thread(target=self.check_condition, args=(case,))
            check_thread.start()
            check_thread.join()
            q.put('stop')

        q = multiprocessing.Queue()
        process = Process(target=do_run)
        process.start()
        q.get()
        process.terminate()
        return self.shared_bool.value


    @abstractmethod
    def blocked(self):
        pass

    def check_condition(self, case : str):
        self.shared_bool.value = self.perform_check(case=case)

    @abstractmethod
    def perform_check(self, case : str) -> bool:
        pass