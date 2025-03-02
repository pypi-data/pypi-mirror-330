import inspect
from typing import Any, Callable, get_type_hints
from dataclasses import dataclass
from typing import Union

class BoundFunction:
    __self__: object


@dataclass
class Argument:
    name: str
    dtype: type

    def set_default_val(self, val: object):
        setattr(self, 'default_val', val)

    def has_default_val(self):
        return hasattr(self, 'default_val')

    def get_default_val(self) -> Any:
        if not self.has_default_val():
            raise AttributeError(f"Argument '{self.name}' has no default value.")
        return getattr(self, 'default_val')



class ModuleInspector:
    @classmethod
    def get_methods(cls, obj : Union[object, type],
                    include_inherited: bool = True,
                    include_private = False,
                    include_magic_methods : bool = False) -> list[Callable]:

        def mthd_ok(mthd_name : str) -> bool:
            if cls.is_magical(mthd_name):
                return include_magic_methods
            elif cls.is_private(mthd_name):
                return include_private
            else:
                return True

        attrs = dir(obj)
        if not include_inherited:
            obj_cls = obj if isinstance(obj, type) else obj.__class__
            parent_attrs = []
            for p in obj_cls.__bases__:
                parent_attrs += dir(p)
            attrs = [name for name in attrs if not name in parent_attrs]
        attr_values = [getattr(obj, name) for name in attrs]

        targeted_methods = []
        for attr_name, value in zip(attrs, attr_values):
            if callable(value) and mthd_ok(attr_name):
                targeted_methods.append(value)

        return targeted_methods

    @staticmethod
    def get_args(func: Union[Callable, BoundFunction], exclude_self : bool = True) -> list[Argument]:
        spec = inspect.getfullargspec(func)
        type_hints = get_type_hints(func)
        if not spec.args:
            return []

        start_index = 1 if exclude_self and spec.args[0] in ['self', 'cls'] else 0
        relevant_arg_names = spec.args[start_index:]
        defaults_mapping = ModuleInspector._get_defaults_mapping(spec=spec)

        def create_arg(name : str):
            dtype = type_hints.get(name)
            is_bound = inspect.ismethod(func)
            if name == 'self' and is_bound:
                dtype = func.__self__.__class__
            if name == 'cls' and is_bound:
                dtype = func.__self__
            if not dtype:
                raise ValueError(f"Type hint for argument '{name}' is missing.")
            argument = Argument(name=name, dtype=dtype)
            if name in defaults_mapping:
                argument.set_default_val(defaults_mapping[name])
            return argument

        return [create_arg(name=name) for name in relevant_arg_names]

    @staticmethod
    def _get_defaults_mapping(spec):
        defaults = spec.defaults or ()
        reversed_args = spec.args[::-1]
        reversed_defaults = defaults[::-1]

        zipped = zip(reversed_args, reversed_defaults)
        return dict(zipped)

    @staticmethod
    def is_magical(name : str):
        return name.startswith('__') and name.endswith('__')

    @staticmethod
    def is_private(name : str):
        return name.startswith('_')
