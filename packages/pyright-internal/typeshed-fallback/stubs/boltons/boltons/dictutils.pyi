from _typeshed import SupportsKeysAndGetItem
from collections.abc import Generator, ItemsView, Iterable, KeysView, ValuesView
from typing import NoReturn, TypeVar, overload
from typing_extensions import Self, TypeAlias

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_T = TypeVar("_T")

class OrderedMultiDict(dict[_KT, _VT]):
    def add(self, k: _KT, v: _VT) -> None: ...
    def addlist(self, k: _KT, v: Iterable[_VT]) -> None: ...
    def clear(self) -> None: ...
    def copy(self) -> Self: ...
    def counts(self) -> Self: ...
    @classmethod
    def fromkeys(cls, keys: _KT, default: _VT | None = None) -> Self: ...  # type: ignore[override]
    @overload  # type: ignore[override]
    def get(self, k: _KT, default: None = None) -> _VT | None: ...
    @overload
    def get(self, k: _KT, default: _VT) -> _VT: ...
    def getlist(self, k: _KT, default: list[_VT] = ...) -> list[_VT]: ...
    def inverted(self) -> Self: ...
    def items(self, multi: bool = False) -> list[tuple[_KT, _VT]]: ...  # type: ignore[override]
    def iteritems(self, multi: bool = False) -> Generator[tuple[_KT, _VT], None, None]: ...
    def iterkeys(self, multi: bool = False) -> Generator[_KT, None, None]: ...
    def itervalues(self, multi: bool = False) -> Generator[_VT, None, None]: ...
    def keys(self, multi: bool = False) -> list[_KT]: ...  # type: ignore[override]
    def pop(self, k: _KT, default: _VT = ...) -> _VT: ...  # type: ignore[override]
    def popall(self, k: _KT, default: _VT = ...) -> list[_VT]: ...
    def poplast(self, k: _KT = ..., default: _VT = ...) -> _VT: ...
    @overload  # type: ignore[override]
    def setdefault(self, k: _KT, default: None = ...) -> _VT | None: ...
    @overload
    def setdefault(self, k: _KT, default: _VT) -> _VT: ...
    def sorted(self, key: _KT | None = None, reverse: bool = False) -> Self: ...
    def sortedvalues(self, key: _KT | None = None, reverse: bool = False) -> Self: ...
    def todict(self, multi: bool = False) -> dict[_KT, _VT]: ...
    def update(self, E: SupportsKeysAndGetItem[_KT, _VT] | Iterable[tuple[_KT, _VT]], **F) -> None: ...  # type: ignore[override]
    def update_extend(self, E: SupportsKeysAndGetItem[_KT, _VT] | Iterable[tuple[_KT, _VT]], **F) -> None: ...
    def values(self, multi: bool = False) -> list[_VT]: ...  # type: ignore[override]
    def viewitems(self) -> ItemsView[_KT, _VT]: ...
    def viewkeys(self) -> KeysView[_KT]: ...
    def viewvalues(self) -> ValuesView[_VT]: ...

OMD: TypeAlias = OrderedMultiDict[_KT, _VT]
MultiDict: TypeAlias = OrderedMultiDict[_KT, _VT]

class FastIterOrderedMultiDict(OrderedMultiDict[_KT, _VT]):  # undocumented
    def iteritems(self, multi: bool = False) -> Generator[tuple[_KT, _VT], None, None]: ...
    def iterkeys(self, multi: bool = False) -> Generator[_KT, None, None]: ...

class OneToOne(dict[_KT, _VT]):
    inv: OneToOne[_VT, _KT]
    def clear(self) -> None: ...
    def copy(self) -> Self: ...
    def pop(self, key: _KT, default: _VT | _T = ...) -> _VT | _T: ...
    def popitem(self) -> tuple[_KT, _VT]: ...
    def setdefault(self, key: _KT, default: _VT | None = None) -> _VT: ...
    @classmethod
    def unique(cls, *a, **kw) -> Self: ...
    def update(self, dict_or_iterable, **kw) -> None: ...  # type: ignore[override]

class ManyToMany(dict[_KT, frozenset[_VT]]):
    data: dict[_KT, set[_VT]]
    inv: dict[_VT, set[_KT]]
    # def __contains__(self, key: _KT): ...
    def __delitem__(self, key: _KT) -> None: ...
    def __eq__(self, other): ...
    def __getitem__(self, key: _KT): ...
    def __init__(
        self, items: ManyToMany[_KT, _VT] | SupportsKeysAndGetItem[_KT, _VT] | tuple[_KT, _VT] | None = None
    ) -> None: ...
    def __iter__(self): ...
    def __len__(self): ...
    def __setitem__(self, key: _KT, vals: Iterable[_VT]) -> None: ...
    def add(self, key: _KT, val: _VT) -> None: ...
    def get(self, key: _KT, default: frozenset[_VT] = ...) -> frozenset[_VT]: ...  # type: ignore[override]
    def iteritems(self) -> Generator[tuple[_KT, _VT], None, None]: ...
    def keys(self): ...
    def remove(self, key: _KT, val: _VT) -> None: ...
    def replace(self, key: _KT, newkey: _KT) -> None: ...
    def update(self, iterable: ManyToMany[_KT, _VT] | SupportsKeysAndGetItem[_KT, _VT] | tuple[_KT, _VT]) -> None: ...  # type: ignore[override]

def subdict(d: dict[_KT, _VT], keep: Iterable[_KT] | None = None, drop: Iterable[_KT] | None = None) -> dict[_KT, _VT]: ...

class FrozenHashError(TypeError): ...  # undocumented

class FrozenDict(dict[_KT, _VT]):
    def __copy__(self) -> Self: ...
    @classmethod
    def fromkeys(cls, keys: Iterable[_KT], value: _VT | None = None) -> Self: ...  # type: ignore[override]
    def updated(self, *a, **kw) -> Self: ...
    # Can't noqa because of https://github.com/plinss/flake8-noqa/pull/30
    # Signature conflicts with superclass, so let's just omit it
    # def __ior__(self, *a, **kw) -> NoReturn: ...
    def __setitem__(self, *a, **kw) -> NoReturn: ...
    def __delitem__(self, *a, **kw) -> NoReturn: ...
    def update(self, *a, **kw) -> NoReturn: ...
    def pop(self, *a, **kw) -> NoReturn: ...
    def popitem(self, *a, **kw) -> NoReturn: ...
    def setdefault(self, *a, **kw) -> NoReturn: ...
    def clear(self, *a, **kw) -> NoReturn: ...
