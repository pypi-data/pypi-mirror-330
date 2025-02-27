from collections.abc import Iterator
from contextlib import contextmanager
from typing import Callable, Literal, Optional, Union, overload

from classiq.interface.exceptions import ClassiqInternalError

from classiq.qmod.quantum_callable import QCallable
from classiq.qmod.quantum_function import (
    BaseQFunc,
    ExternalQFunc,
    GenerativeQFunc,
    QFunc,
)

_GENERATIVE_SWITCH = False


@contextmanager
def set_global_generative_switch() -> Iterator[None]:
    global _GENERATIVE_SWITCH
    previous = _GENERATIVE_SWITCH
    _GENERATIVE_SWITCH = True
    try:
        yield
    finally:
        _GENERATIVE_SWITCH = previous


@overload
def qfunc(func: Callable) -> QFunc: ...


@overload
def qfunc(
    *,
    external: Literal[True],
    synthesize_separately: Literal[False] = False,
) -> Callable[[Callable], ExternalQFunc]: ...


@overload
def qfunc(
    *,
    generative: Literal[True],
    synthesize_separately: bool = False,
) -> Callable[[Callable], GenerativeQFunc]: ...


@overload
def qfunc(*, synthesize_separately: bool) -> Callable[[Callable], QFunc]: ...


def qfunc(
    func: Optional[Callable] = None,
    *,
    external: bool = False,
    generative: bool = False,
    synthesize_separately: bool = False,
) -> Union[Callable[[Callable], QCallable], QCallable]:
    def wrapper(func: Callable) -> QCallable:
        qfunc: BaseQFunc
        if generative or _GENERATIVE_SWITCH:
            qfunc = GenerativeQFunc(func)
        elif external:
            if synthesize_separately:
                raise ClassiqInternalError(
                    "External functions can't be marked as synthesized separately"
                )
            return ExternalQFunc(func)
        else:
            qfunc = QFunc(func)
        if synthesize_separately:
            qfunc.update_compilation_metadata(should_synthesize_separately=True)
        return qfunc

    if func is not None:
        return wrapper(func)

    return wrapper
