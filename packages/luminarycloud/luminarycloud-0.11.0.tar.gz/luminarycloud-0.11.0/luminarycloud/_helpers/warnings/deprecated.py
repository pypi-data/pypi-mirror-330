import warnings
from functools import wraps
from typing import Callable, TypeVar

C = TypeVar("C")


def deprecated(reason: str, version: str) -> Callable[[C], C]:
    """
    Mark a class or function as deprecated.

    Parameters
    ----------
    reason : str
        The reason for deprecation.
    version : str
        The version in which the class or function was deprecated.
    """

    def decorator(f: Callable | type[C]) -> Callable | type[C]:
        if isinstance(f, type):
            return _deprecated_class(f, reason, version)
        else:
            return _deprecated_function(f, reason, version)

    return decorator


def _deprecated_class(cls: type[C], reason: str, version: str) -> type[C]:
    old_init = cls.__init__

    @wraps(old_init)
    def new_init(self, *args, **kwargs):
        warnings.warn(
            f"{cls.__name__} is deprecated after version {version}: {reason}",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return old_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls


def _deprecated_function(f: Callable, reason: str, version: str) -> Callable:
    @wraps(f)
    def new_func(*args, **kwargs):
        warnings.warn(
            f"{f.__name__}() is deprecated after version {version}: {reason}",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return f(*args, **kwargs)

    return new_func
