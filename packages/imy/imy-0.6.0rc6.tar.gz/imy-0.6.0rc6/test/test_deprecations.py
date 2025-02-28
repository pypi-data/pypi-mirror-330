import warnings
from dataclasses import dataclass

import imy.deprecations


def test_deprecated_class():
    @imy.deprecations.deprecated(since="1.1", replacement="Bar")
    class Foo:
        pass

    with warnings.catch_warnings(record=True) as warnings_list:
        Foo()

    assert len(warnings_list) == 1


def test_deprecated_function_and_parameter():
    @imy.deprecations.deprecated(
        since="1.2",
        will_be_removed_in_version="1.5",
        description="It causes undefined behavior",
    )
    @imy.deprecations.parameter_renamed(
        since="1.3", old_name="old_param", new_name="param"
    )
    def foo(param: int):
        return param

    with warnings.catch_warnings(record=True) as warnings_list:
        assert foo(3) == 3

    assert len(warnings_list) == 1

    with warnings.catch_warnings(record=True) as warnings_list:
        assert foo(old_param=5) == 5  # type: ignore

    assert len(warnings_list) == 2


def test_parameter_remapping():
    @imy.deprecations.parameter_remapped(
        since="1.3",
        old_name="old_param",
        new_name="param",
        remap=str,
    )
    def foo(param: str):
        return param

    with warnings.catch_warnings(record=True) as warnings_list:
        assert foo("hi") == "hi"

    assert len(warnings_list) == 0

    with warnings.catch_warnings(record=True) as warnings_list:
        assert foo(old_param=5) == "5"  # type: ignore

    assert len(warnings_list) == 1


def test_dataclass_parameter_deprecation():
    @imy.deprecations.parameter_renamed(since="0.9.3", old_name="foo", new_name="bar")
    @dataclass
    class MyClass:
        bar: int

    assert MyClass(foo=5).bar == 5  # type: ignore


def test_stacktrace():
    @imy.deprecations.parameter_renamed(since="0.9.3", old_name="old", new_name="new")
    @imy.deprecations.parameter_renamed(since="0.9.3", old_name="foo", new_name="bar")
    def my_func(*, bar, new):
        pass

    with warnings.catch_warnings(record=True) as warnings_list:
        exec("""my_func(old=3, foo='hi')""", {"my_func": my_func})

    assert len(warnings_list) == 2
    for warning in warnings_list:
        assert warning.filename == "<string>"
        assert warning.lineno == 1
