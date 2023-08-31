from types import ModuleType
from importlib import import_module

import madlad.parameters
import madlad.utils


# python/util/lazy_loader.py
class LazyLoader(ModuleType):
    def __init__(self, local_name, parent_module_globals, name):
        self._local_name = local_name
        self._parent_module_globals = parent_module_globals
        super().__init__(name)

    def _load(self):
        module = import_module(self.__name__)
        self._parent_module_globals[self._local_name] = module
        self.__dict__.update(module.__dict__)
        return module

    def __getattr__(self, item):
        module = self._load()
        return getattr(module, item)

    def __dir__(self):
        module = self._load()
        return dir(module)


parameters = LazyLoader('data', globals(), 'madlad.parameters')
utils = LazyLoader('graphs', globals(), 'madlad.utils')

__version__ = 'alpha0.1'


__all__ = [
    'madlad',
    '__version__',
]