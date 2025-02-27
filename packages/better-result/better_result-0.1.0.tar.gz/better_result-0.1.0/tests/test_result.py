from __future__ import annotations

from typing import Any
from typing import Never
from unittest import mock

import pytest

from better_result import Err
from better_result import Ok
from better_result import Result
from better_result import UnwrapError
from better_result import as_result
from better_result import is_err
from better_result import is_ok


class TestFactories:
    def test_ok_init(self):
        instance = Ok(1)
        assert instance.ok_value == 1
        assert instance.ok() == 1
        assert instance.err() is None
        assert instance.is_ok() is True
        assert instance.is_err() is False

    def test_err_init(self):
        instance = Err("error")

        assert instance.err_value == "error"
        assert instance.ok() is None
        assert instance.err() == "error"
        assert instance.is_ok() is False
        assert instance.is_err() is True

    @pytest.mark.parametrize("val", [1, "test", {}, []])
    def test_repr(self, val: object):
        instance = Ok(val)
        assert repr(instance) == f"Ok({val!r})"
        assert eval(repr(instance)) == instance

    def test_eq(self):
        assert Ok(1) == Ok(1)
        assert Ok(1) != Err(1)
        assert Ok(1) != Ok(2)
        assert not (Ok(1) != Ok(1))
        assert Ok(1) != "abc"
        assert Ok("0") != Ok(0)

    def test_hash(self) -> None:
        assert len({Ok(1), Err("2"), Ok(1), Err("2")}) == 2
        assert len({Ok(1), Ok(2)}) == 2
        assert len({Ok("a"), Err("a")}) == 2

    def test_ok_expect(self):
        instance = Ok(1)
        assert instance.expect("error") == 1
        with pytest.raises(UnwrapError) as exc:
            instance.expect_err("error")
        assert exc.match("error")

    def test_err_expect(self):
        instance = Err("problem")
        assert instance.expect_err("error") == "problem"
        with pytest.raises(UnwrapError) as exc:
            instance.expect("error")
        assert exc.match("error")

    def test_ok_unwrap(self):
        instance = Ok(1)
        assert instance.unwrap() == 1
        with pytest.raises(UnwrapError) as exc:
            instance.unwrap_err()
        assert exc.match(r"Called `Result.unwrap_err\(\)` on an `Ok` value")
        assert instance.unwrap_or_raise(RuntimeError) == 1
        assert instance.unwrap_or(2) == 1
        assert instance.unwrap_or_else(cb_mock := mock.MagicMock()) == 1
        cb_mock.assert_not_called()

    def test_err_unwrap(self):
        instance = Err("Some error")
        assert instance.unwrap_err() == "Some error"
        with pytest.raises(UnwrapError) as exc:
            instance.unwrap()
        assert exc.match(r"Called `Result.unwrap\(\)` on an `Err` value")
        with pytest.raises(RuntimeError) as exc:
            instance.unwrap_or_raise(RuntimeError)
        assert exc.match("Some error")
        assert instance.unwrap_or(1) == 1
        assert instance.unwrap_or_else(cb_mock := mock.MagicMock(return_value=1)) == 1
        cb_mock.assert_called_once_with("Some error")

    def test_ok_map(self):
        instance = Ok(1)
        assert instance.map(cb_mock := mock.MagicMock(return_value=2)).ok_value == 2
        cb_mock.assert_called_once_with(1)
        assert instance.map_or(None, cb_mock := mock.MagicMock(return_value=3)) == 3
        cb_mock.assert_called_once_with(1)
        assert (
            instance.map_or_else(
                default_cb_mock := mock.MagicMock(), map_func_mock := mock.MagicMock(return_value=4)
            )
            == 4
        )
        default_cb_mock.assert_not_called()
        map_func_mock.assert_called_once_with(1)
        assert instance.map_err(cb_mock := mock.MagicMock()) is instance
        cb_mock.assert_not_called()

    def test_err_map(self):
        instance = Err("Some error")
        assert instance.map(cb_mock := mock.MagicMock()) is instance
        cb_mock.assert_not_called()
        assert instance.map_or(None, cb_mock := mock.MagicMock()) is None
        cb_mock.assert_not_called()
        assert (
            instance.map_or_else(
                default_cb_mock := mock.MagicMock(return_value="Another Error"),
                map_func_mock := mock.MagicMock(return_value=4),
            )
            == "Another Error"
        )
        default_cb_mock.assert_called_once_with()
        map_func_mock.assert_not_called()

    def test_ok_and_them(self):
        instance = Ok(1)
        result = instance.and_then(cb_mock := mock.MagicMock(return_value=Ok(2)))
        assert is_ok(result)
        assert result.ok_value == 2
        cb_mock.assert_called_once_with(1)

        def sq_then_to_string(x: int) -> Result[str, str]:
            if (squared := x * x) > (2**32 - 1):
                return Err("Overflow")
            return Ok(str(squared))

        assert Ok(2).and_then(sq_then_to_string) == Ok("4")
        assert Ok(1_000_000).and_then(sq_then_to_string) == Err("Overflow")
        assert Err("not a number").and_then(sq_then_to_string) == Err("not a number")

    def test_or_else(self):
        def sq(n: int) -> Result[int, Never]:
            return Ok(n * n)

        def err(n: int):
            return Err(n)

        assert Ok(2).or_else(sq).or_else(sq) == Ok(2)
        assert Ok(2).or_else(err).or_else(sq) == Ok(2)
        assert Err(3).or_else(sq).or_else(err) == Ok(9)
        assert Err(3).or_else(err).or_else(err) == Err(3)

    def test_inspect(self):
        assert Ok(1).inspect(mock_inspect := mock.MagicMock()) == Ok(1)
        mock_inspect.assert_called_once_with(1)

        assert Err("error").inspect(mock_inspect := mock.MagicMock()) == Err("error")
        mock_inspect.assert_not_called()

        assert Ok(1).inspect_err(mock_inspect := mock.MagicMock()) == Ok(1)
        mock_inspect.assert_not_called()

        assert Err("error").inspect_err(mock_inspect := mock.MagicMock()) == Err("error")
        mock_inspect.assert_called_once_with("error")

def test_as_result_decorator():
    @as_result(ValueError)
    def safe_parse_int(v: Any) -> int:
        return int(v)

    assert safe_parse_int("1") == Ok(1)
    result = safe_parse_int("a")
    assert is_err(result)
    assert isinstance(result.err_value, ValueError)
