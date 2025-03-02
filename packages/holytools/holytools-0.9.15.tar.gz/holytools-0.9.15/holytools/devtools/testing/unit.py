import inspect
import logging
import unittest
import unittest.mock
from logging import Logger
from typing import Optional, Callable

from holytools.logging import LoggerFactory
from .result import UnitTestCase
from .runner import Runner


# ---------------------------------------------------------

class Unittest(UnitTestCase):
    _logger : Logger = None

    @classmethod
    def execute_all(cls, manual_mode : bool = True, trace_resourcewarning : bool = False):
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        runner = Runner(logger=cls.get_logger(), is_manual=manual_mode, test_name=cls.__name__)
        tracemalloc_depth = 10 if trace_resourcewarning else 0
        results = runner.run(testsuite=suite, tracemalloc_depth=tracemalloc_depth)
        results.print_summary()

        return results

    @classmethod
    def get_logger(cls) -> Logger:
        if not cls._logger:
            cls._logger = LoggerFactory.get_logger(include_location=False, include_timestamp=False, name=cls.__name__)
        return cls._logger

    @classmethod
    def log(cls, msg : str, level : int = logging.INFO):
        cls.get_logger().log(msg=f'{msg}', level=level)

    def warning(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.WARNING
        self._logger.log(msg=msg, *args, **kwargs)

    def error(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.ERROR
        self._logger.log(msg=msg, *args, **kwargs)

    def critical(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.CRITICAL
        self._logger.log(msg=msg, *args, **kwargs)

    def info(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.INFO
        self._logger.log(msg=msg, *args, **kwargs)


    # ---------------------------------------------------------
    # assertions

    def assertEqual(self, first : object, second : object, msg : Optional[str] = None):
        if not first == second:
            first_str = str(first).__repr__()
            second_str = str(second).__repr__()
            if msg is None:
                msg = (f'Tested expressions should match:'
                       f'\nFirst : {first_str} ({type(first)})'
                       f'\nSecond: {second_str} ({type(second)})')
            raise AssertionError(msg)

    def assertSame(self, first : dict, second : dict, msg : Optional[str] = None):
        """Checks whether contents of dicts first and second are the same"""
        for key in first:
            first_obj = first[key]
            second_obj = second[key]
            self.assertSameElementary(type(first_obj), type(second_obj))
            if isinstance(first_obj, dict):
                self.assertSame(first_obj, second_obj, msg=msg)
            elif isinstance(first_obj, list):
                for i in range(len(first_obj)):
                    self.assertSameElementary(first_obj[i], second_obj[i])
            else:
                self.assertSameElementary(first_obj, second_obj)

    def assertSameElementary(self, first : object, second : object):
        if isinstance(first, float) and isinstance(second, float):
            self.assertSameFloat(first, second)
        else:
            self.assertEqual(first, second)

    @staticmethod
    def assertSameFloat(first : float, second : float, msg : Optional[str] = None):
        if first != first:
            same_float = second != second
        else:
            same_float = first == second
        if not same_float:
            first_str = str(first).__repr__()
            second_str = str(second).__repr__()
            if msg is None:
                msg = (f'Tested floats should match:'
                       f'\nFirst : {first_str} ({type(first)})'
                       f'\nSecond: {second_str} ({type(second)})')
            raise AssertionError(msg)


    def assertIn(self, member : object, container, msg : Optional[str] = None):
        if not member in container:
            member_str = str(member).__repr__()
            container_str = str(container).__repr__()
            if msg is None:
                msg = f'{member_str} not in {container_str}'
            raise AssertionError(msg)


    def assertIsInstance(self, obj : object, cls : type, msg : Optional[str] = None):
        if not isinstance(obj, cls):
            obj_str = str(obj).__repr__()
            cls_str = str(cls).__repr__()
            if msg is None:
                msg = f'{obj_str} not an instance of {cls_str}'
            raise AssertionError(msg)


    def assertTrue(self, expr : bool, msg : Optional[str] = None):
        if not expr:
            if msg is None:
                msg = f'Tested expression should be true'
            raise AssertionError(msg)


    def assertFalse(self, expr : bool, msg : Optional[str] = None):
        if expr:
            if msg is None:
                msg = f'Tested expression should be false'
            raise AssertionError(msg)





    @staticmethod
    def patch_module(original: type | Callable, replacement: type | Callable):
        module_path = inspect.getmodule(original).__name__
        qualified_name = original.__qualname__
        frame = inspect.currentframe().f_back
        caller_module = inspect.getmodule(frame)

        try:
            # corresponds to "from [caller_module] import [original]
            _ = getattr(caller_module, qualified_name)
            full_path = f"{caller_module.__name__}.{qualified_name}"
        except Exception:
            # corresponds to import [caller_module].[original]
            full_path = f"{module_path}.{qualified_name}"

        # print(f'Full path = {full_path}')
        def decorator(func):
            return unittest.mock.patch(full_path, replacement)(func)

        return decorator


