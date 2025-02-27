from __future__ import annotations

import functools
from collections.abc import Awaitable
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from typing import Generic
from typing import Literal
from typing import Never
from typing import NoReturn
from typing import Self
from typing import cast

from typing_extensions import TypeIs
from typing_extensions import TypeVar

_R = TypeVar("_R", covariant=True, default=Never)
_E = TypeVar("_E", covariant=True, default=Never)

type Result[R, E] = Ok[R, E] | Err[E, R]
"""
A simple `Result` type inspired by Rust.
Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html)
have been implemented, only the ones that make sense in the Python context.
"""


@dataclass(slots=True, frozen=True)
class Some[T]:
    """
    Similar to Rust's [`Option::Some`](https://doc.rust-lang.org/std/option/enum.Option.html),
    this identifies a value as being present, and provides a way to access it.

    Generally used in a union with `None` to differentiate between
    "some value which could be None" and no value.

    example:
    ```python
    def get_value() -> Some[int | float | str | bool | None] | None: ...

    # Using `isinstance` as a type guard
    if isinstance(get_value(), Some):
        # Do something when value is present
    else:
        # Do something when value is not present

    # Using Structural pattern matching
    match get_value():
        case Some(value):
            # Do something when value is present
        case None:
            # Do something when value is not present
    ```
    """

    value: T


class Ok(Generic[_R, _E]):
    """
    A value that indicates success and which stores arbitrary data for the return value.
    """

    __match_args__ = ("ok_value",)
    __slots__ = ("_value",)

    def __init__(self, value: _R) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"Ok({self._value!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ok) and self._value == cast(Ok[Any, Any], other)._value

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((True, self._value))

    def is_ok(self) -> Literal[True]:
        return True

    def is_err(self) -> Literal[False]:
        return False

    def ok(self) -> _R:
        """
        Return the value.
        """
        return self._value

    def err(self) -> None:
        """
        Return `None`.
        """
        return None

    @property
    def ok_value(self) -> _R:
        return self._value

    def expect(self, _: str, /) -> _R:
        return self._value

    def expect_err(self, message: str) -> NoReturn:
        """
        Raise an UnwrapError since this type is `Ok`
        """
        raise UnwrapError(self, message)

    def unwrap(self) -> _R:
        """
        Return the value.
        """
        return self._value

    def unwrap_err(self) -> NoReturn:
        """
        Raise an UnwrapError since this type is `Ok`
        """
        raise UnwrapError(self, "Called `Result.unwrap_err()` on an `Ok` value")

    def unwrap_or(self, _: object, /) -> _R:
        return self._value

    def unwrap_or_else(self, _: Callable[[_E], Any], /) -> _R:
        return self._value

    def unwrap_or_raise(self, exc: object, /) -> _R:
        return self._value

    def map[U](self, map_func: Callable[[_R], U], /) -> Ok[U, _E]:
        """
        Maps a `Result[T, E]` to `Result[U, E]` by applying a function `func`
        with signature `(T) -> U` to a contained `Ok` value, leaving an `Err`
        value untouched.

        example:
        ```python
        import random


        def my_function() -> better_result.Result[int, str]:
            if random.random() < 0.5:
                return better_result.Ok(2)
            return better_result.Err("Something Bad Happened")


        mapped_result = my_function().map(lambda n: n**2)
        if better_result.is_ok(mapped_result):
            assert better_result.ok_value == 4
        else:
            assert better_result.err_value == "Something Bad Happened"
        ```
        """
        return Ok(map_func(self._value))

    async def map_async[U](self, map_func: Callable[[_R], Awaitable[U]], /) -> Ok[U, _E]:
        """
        The contained result is `Ok`, so return the result of `func` with the
        original value passed in
        """
        return Ok(await map_func(self._value))

    def map_or[U](self, default_if_err: object, map_func: Callable[[_R], U], /) -> U:
        """
        The contained result is `Ok`, so return the original value mapped to a new
        value using the passed in function.
        """
        return map_func(self._value)

    def map_or_else[U](self, default_cb: Callable[[], object], map_func: Callable[[_R], U], /) -> U:
        """
        The contained result is `Ok`, so return original value mapped to
        a new value using the passed in `map_func` function.
        """
        return map_func(self._value)

    def map_err(self, _: Callable[[_E], Any], /) -> Self:
        """
        The contained result is `Ok`, so return `Ok` with the original value
        """
        return self

    def and_then[U, V](self, func: Callable[[_R], Result[U, V]], /) -> Result[U, _E]:
        """
        Calls `func` if the result is `Ok`, leaving an `Err` value untouched.

        This is different from `map` in the sense that callback signature returns
        a result, so this can be used for chaining functions.

        example:

        ```python
        def open_file(path: str) -> Result[IO[str], str]: ...
        def read_lines(io: IO[str]) -> Result[list[str], str]: ...


        def fn():
            return open_file("path/to/file.txt").and_then(read_lines)


        # The code for `fn` above would be equivalent to writing something like this:
        def fn2():
            match open_file("path/to/file.txt"):
                case Ok(value):
                    return read_lines(value)
                case Err(err_value):
                    return Err(err_value)


        match fn():
            case Ok(value):
                assert_type(
                    value,
                    list[str],
                )
            case Err(err):
                # err can be from `open_file` or `read_lines`
                assert_type(err, str)
        ```
        """
        return cast(Result[U, _E], func(self._value))

    async def and_then_async[U](
        self, func: Callable[[_R], Awaitable[Result[U, _E]]], /
    ) -> Result[U, _E]:
        """
        Same as `and_then` but accepts async functions
        """
        return await func(self._value)

    def or_else[U, V](self, func: Callable[[_E], Result[U, V]], /) -> Ok[_R, V]:
        """
        Calls `func` if the result is `Err`, leaving an `OK` value untouched.

        This is similar to `and_then` but it operates on the `Err` instead of `Ok`,
        they can be combined for control flow based on result values.

        example:
        ```
        def open_file(path: str) -> Result[IO[str], str]: ...
        def read_lines(io: IO[str]) -> Result[list[str], str]: ...


        result: Result[list[str], str] = (
            open_file("path/to/file.txt")
            .or_else(lambda _err: open_file("try/another/file.txt"))
            .and_then(read_lines)
        )

        # OR
        result: Result[list[str], str] = (
            open_file("path/to/file.txt")
            .and_then(read_lines)
            .or_else(lambda _: open_file("try/another/file.txt").and_then(read_lines))
        )
        ```
        """
        return cast(Ok[_R, V], self)

    def inspect(self, func: Callable[[_R], Any], /) -> Self:
        """
        Calls a function with the contained value if `Ok`.
        Returns the original result.
        """
        func(self._value)
        return self

    def inspect_err(self, func: Callable[[_E], Any], /) -> Self:
        """
        Calls a function with the contained value if `Err`.
        Returns the original result.
        """
        return self


class Err(Generic[_E, _R]):
    """
    A value that signifies failure and which stores arbitrary data for the error.
    """

    __match_args__ = ("err_value",)
    __slots__ = ("_value",)

    def __init__(self, value: _E) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"Err({repr(self._value)})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Err) and self._value == cast(Err[Any, Any], other)._value

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((False, self._value))

    def is_ok(self) -> Literal[False]:
        return False

    def is_err(self) -> Literal[True]:
        return True

    def ok(self) -> None:
        """
        Return `None`.
        """
        return None

    def err(self) -> _E:
        """
        Return the error.
        """
        return self._value

    @property
    def err_value(self) -> _E:
        """
        Return the inner value.
        """
        return self._value

    def expect(self, message: str, /) -> NoReturn:
        """
        Raises an `UnwrapError` with given message
        """
        exc = UnwrapError(
            self,
            f"{message}: {self._value!r}",
        )
        if isinstance(self._value, BaseException):
            raise exc from self._value
        raise exc

    def expect_err(self, _: str, /) -> _E:
        """
        Return the inner value
        """
        return self._value

    def unwrap(self) -> NoReturn:
        """
        Raises an `UnwrapError`.
        """
        exc = UnwrapError(
            self,
            f"Called `Result.unwrap()` on an `Err` value: {self._value!r}",
        )
        if isinstance(self._value, BaseException):
            raise exc from self._value
        raise exc

    def unwrap_err(self) -> _E:
        """
        Return the inner value
        """
        return self._value

    def unwrap_or[U](self, default: U, /) -> U:
        """
        Return `default`.
        """
        return default

    def unwrap_or_else[U](self, func: Callable[[_E], U], /) -> U:
        """
        The contained result is ``Err``, so return the result of applying
        ``func`` to the error value.
        """
        return func(self._value)

    def unwrap_or_raise[Exc: BaseException](self, exc: type[Exc], /) -> NoReturn:
        """
        The contained result is ``Err``, so raise the exception with the value.
        """
        raise exc(self._value)

    def map(self, func: Callable[[_R], Any], /) -> Self:
        """
        Return `Err` with the same value
        """
        return self

    async def map_async(self, func: Callable[[_R], Any]) -> Self:
        """
        The contained result is `Ok`, so return the result of `func` with the
        original value passed in
        """
        return self

    def map_or[U](self, default: U, func: Callable[[_R], Any], /) -> U:
        """
        Return the default value
        """
        return default

    def map_or_else[U](self, default_op: Callable[[], U], func: Callable[[_R], Any], /) -> U:
        """
        Return the result of the default operation
        """
        return default_op()

    def map_err[U](self, func: Callable[[_E], U], /) -> Err[U, _R]:
        """
        The contained result is `Err`, so return `Err` with original error mapped to
        a new value using the passed in function.
        """
        return Err(func(self._value))

    def and_then[U, V](self, func: Callable[[_R], Result[U, V]], /) -> Err[_E, U]:
        """
        The contained result is `Err`, so return `Err` with the original value
        """
        return cast(Err[_E, U], self)

    async def and_then_async[U, V](self, func: Callable[[_R], Awaitable[Result[U, V]]]) -> Err[_E, U]:
        """
        The contained result is `Err`, so return `Err` with the original value
        """
        return cast(Err[_E, U], self)

    def or_else[U, S](self, func: Callable[[_E], Result[U, S]], /) -> Result[U, S]:
        """
        The contained result is `Err`, so return the result of `func` with the
        original value passed in
        """
        return func(self._value)

    def inspect(self, func: Callable[[_R], Any]) -> Self:
        """
        Calls a function with the contained value if `Ok`. Returns the original result.
        """
        return self

    def inspect_err(self, func: Callable[[_E], Any]) -> Self:
        """
        Calls a function with the contained value if `Err`. Returns the original result.
        """
        func(self._value)
        return self


class UnwrapError(Exception):
    """
    Exception raised from `.unwrap_<...>` and `.expect_<...>` calls.

    The original `Result` can be accessed via the `.result` attribute, but
    this is not intended for regular use, as type information is lost:
    `UnwrapError` doesn't know about both `T` and `E`, since it's raised
    from `Ok()` or `Err()` which only knows about either `T` or `E`,
    not both.
    """

    _result: Result[object, object]

    def __init__(self, result: Result[object, object], message: str) -> None:
        self._result = result
        super().__init__(message)

    @property
    def result(self) -> Result[Any, Any]:
        """Original `Result` that caused the error."""
        return self._result


def as_result[**P, U, TBE: BaseException](
    *exceptions: type[TBE],
) -> Callable[[Callable[P, U]], Callable[P, Result[U, TBE]]]:
    """
    A decorator to turn a function into one that returns a `Result`.

    Regular return values are turned into `Ok(return_value)`.
    Raised exceptions of the specified exception type(s) are turned into `Err(exc)`.
    """
    import inspect

    if not exceptions or not all(
        inspect.isclass(exception) and issubclass(exception, BaseException) for exception in exceptions
    ):
        raise TypeError("as_result() requires one or more exception types")

    def decorator(f: Callable[P, U]) -> Callable[P, Result[U, TBE]]:
        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[U, TBE]:
            try:
                return Ok(f(*args, **kwargs))
            except exceptions as exc:
                return Err(exc)

        return wrapper

    return decorator


def as_async_result[**P, U, TBE: BaseException](
    *exceptions: type[TBE],
) -> Callable[[Callable[P, Awaitable[U]]], Callable[P, Awaitable[Result[U, TBE]]]]:
    """
    Make a decorator to turn an async function into one that returns a ``Result``.
    Regular return values are turned into ``Ok(return_value)``. Raised
    exceptions of the specified exception type(s) are turned into ``Err(exc)``.
    """
    import inspect

    if not exceptions or not all(
        inspect.isclass(exception) and issubclass(exception, BaseException) for exception in exceptions
    ):
        raise TypeError("as_result() requires one or more exception types")

    def decorator(f: Callable[P, Awaitable[U]]) -> Callable[P, Awaitable[Result[U, TBE]]]:
        """
        Decorator to turn a function into one that returns a ``Result``.
        """

        @functools.wraps(f)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[U, TBE]:
            try:
                return Ok(await f(*args, **kwargs))
            except exceptions as exc:
                return Err(exc)

        return async_wrapper

    return decorator


def is_ok[T, E](result: Result[T, E]) -> TypeIs[Ok[T, E]]:
    """A type guard to check if a result is an `Ok`

    Usage:

    ``` python
    r: Result[int, str] = get_a_result()
    if is_ok(r):
        r  # r is of type Ok[int]
    elif is_err(r):
        r  # r is of type Err[str]
    ```

    """
    return result.is_ok()


def is_err[T, U](result: Result[T, U]) -> TypeIs[Err[U, T]]:
    """A type guard to check if a result is an `Err`

    Usage:

    ``` python
    r: Result[int, str] = get_a_result()
    if is_ok(r):
        r  # r is of type Ok[int]
    elif is_err(r):
        r  # r is of type Err[str]
    ```

    """
    return result.is_err()
