import imy.deprecations
import imy.docstrings


def _documented_function_names(docs: imy.docstrings.ClassDocs) -> set[str]:
    return set(docs.functions)


def _documented_attribute_names(docs: imy.docstrings.ClassDocs) -> set[str]:
    return set(docs.attributes)


class Parent:
    """
    # Leading Headings 1 are stripped

    This is the summary.

    This is the details. They can be very long and span multiple lines. They can
    even contain multiple paragraphs.

    Just like this one.

    ## Heading 2

    Any non-key sections are also part of the details.

    This is the end of the details.

    ## Attributes

    int_attribute: <int>

    `float_attribute`: <float>

    str_attribute: <str>

    ## Metadata

    public: False
    """

    int_attribute: int
    float_attribute: float
    str_attribute: str

    def __init__(self, foo, bar, baz):
        pass

    @property
    def bytes_property(self) -> bytes:
        """
        This is the getter function of `bytes_property`
        """
        return b""

    @bytes_property.setter
    def bytes_property(self, value: str | bytes) -> None:
        """
        This is the setter function of `bytes_property`
        """
        _ = value

    def numeric_function(self, x: int) -> float:
        """
        <function summary>

        <function details>

        ## Parameters

        x: <int>

        ## Raises

        `ValueError`: <raise-value-error>
        """
        return float(x)

    def overridden_function(self) -> float:
        """
        docstring for `overridden_function`
        """
        return 1.5

    def _private_because_of_underscore(self):
        pass

    def private_because_of_metadata(self):
        """
        ## Metadata

        `public`: False
        """

    def __str__(self) -> str:
        return "<Parent object>"


class Child(Parent):
    """
    Children are parents too!

    ## Attributes

    bool_attribute: <bool>

    ## Metadata

    public: True

    experimental: True
    """

    bool_attribute: bool

    async def list_function(self, x: str) -> list:
        """
        <function summary>

        <function details>

        ## Parameters

        x: <str>
        """
        return [x]

    def overridden_function(self) -> int:
        return 1


def test_parse_class_docstring() -> None:
    docs = imy.docstrings.ClassDocs.from_class(Parent)

    assert docs.name == "Parent"
    assert docs.summary == "This is the summary."

    assert docs.details is not None
    assert docs.details.startswith("This is the details.")
    assert docs.details.endswith("This is the end of the details.")

    assert _documented_function_names(docs) == {
        "__init__",
        "numeric_function",
        "overridden_function",
    }

    init_function_docs = docs.functions["__init__"]
    assert init_function_docs.owner is docs
    assert init_function_docs.name == "__init__"
    assert init_function_docs.synchronous is True
    assert init_function_docs.return_type is imy.docstrings.UNSET
    assert init_function_docs.summary is None
    assert init_function_docs.details is None

    numeric_function_docs = docs.functions["numeric_function"]
    assert numeric_function_docs.owner is docs
    assert numeric_function_docs.name == "numeric_function"
    assert numeric_function_docs.synchronous is True
    assert numeric_function_docs.return_type is float
    assert numeric_function_docs.summary == "<function summary>"
    assert numeric_function_docs.details == "<function details>"

    assert len(numeric_function_docs.parameters) == 2
    param1, param2 = numeric_function_docs.parameters.values()

    assert param1.owner is numeric_function_docs
    assert param1.name == "self"

    assert param2.owner is numeric_function_docs
    assert param2.name == "x"
    assert param2.type is int
    assert param2.description == "<int>"

    overridden_function_docs = docs.functions["overridden_function"]
    assert overridden_function_docs.owner is docs
    assert overridden_function_docs.name == "overridden_function"
    assert overridden_function_docs.synchronous is True
    assert overridden_function_docs.return_type is float
    assert overridden_function_docs.summary == "docstring for `overridden_function`"
    assert overridden_function_docs.details is None

    assert len(numeric_function_docs.raises) == 1
    assert numeric_function_docs.raises[0] == (
        "ValueError",
        "<raise-value-error>",
    )

    assert _documented_attribute_names(docs) == {
        "int_attribute",
        "float_attribute",
        "str_attribute",
    }

    for attr in docs.attributes.values():
        assert attr.owner is docs
        assert attr.type is not None
        assert attr.description is not None
        assert attr.description.strip() == f"<{attr.type.__name__}>"  # type: ignore

    for prop in docs.properties.values():
        assert prop.owner is docs

        assert prop.getter.owner is prop

        assert prop.setter is not None
        assert prop.setter.owner is prop

    assert docs.metadata.public is False
    assert docs.metadata.experimental is False


def test_parse_class_docstring_with_inheritance() -> None:
    docs = imy.docstrings.ClassDocs.from_class(Child)

    assert docs.name == "Child"
    assert docs.summary == "Children are parents too!"
    assert docs.details is None

    assert _documented_function_names(docs) == {
        "__init__",
        "numeric_function",
        "list_function",
        "overridden_function",
    }

    for func in docs.functions.values():
        assert func.owner is docs

        if func.name == "__init__":
            assert func.synchronous is True
            assert func.return_type is imy.docstrings.UNSET
            assert func.summary is None
            assert func.details is None

            assert len(func.parameters) == 4
            param1, param2, param3, param4 = func.parameters.values()

            assert param1.name == "self"

            assert param2.name == "foo"
            assert param2.type is imy.docstrings.UNSET
            assert param2.description is None

            assert param3.name == "bar"
            assert param3.type is imy.docstrings.UNSET
            assert param3.description is None

            assert param4.name == "baz"
            assert param4.type is imy.docstrings.UNSET
            assert param4.description is None

        elif func.name == "numeric_function":
            assert func.synchronous is True
            assert func.return_type is float
            assert func.summary == "<function summary>"
            assert func.details == "<function details>"

            assert len(func.parameters) == 2
            param1, param2 = func.parameters.values()

            assert param1.name == "self"

            assert param2.name == "x"
            assert param2.type is int
            assert param2.description == "<int>"

            assert len(func.raises) == 1
            assert func.raises[0] == ("ValueError", "<raise-value-error>")

        elif func.name == "list_function":
            assert func.synchronous is False
            assert func.return_type is list
            assert func.summary == "<function summary>"
            assert func.details == "<function details>"

            assert len(func.parameters) == 2
            param1, param2 = func.parameters.values()

            assert param1.name == "self"

            assert param2.name == "x"
            assert param2.type is str
            assert param2.description == "<str>"

            assert len(func.raises) == 0

        elif func.name == "overridden_function":
            assert func.owner is docs
            assert func.synchronous is True
            assert func.return_type is int
            assert func.summary == "docstring for `overridden_function`"
            assert func.details is None

        else:
            assert False, f"Unexpected function: {func.name}"

    assert _documented_attribute_names(docs) == {
        "int_attribute",
        "float_attribute",
        "str_attribute",
        "bool_attribute",
    }

    for attr in docs.attributes.values():
        assert attr.owner is docs
        assert attr.type is not None
        assert attr.description is not None
        assert attr.description.strip() == f"<{attr.type.__name__}>"  # type: ignore

    assert docs.metadata.public is True
    assert docs.metadata.experimental is True


def test_parse_module() -> None:
    from test import docstrings_test_package

    module_docs = imy.docstrings.ModuleDocs.from_module(docstrings_test_package)

    assert module_docs.object is docstrings_test_package
    assert module_docs.name == "docstrings_test_package"
    assert module_docs.owner is None
    assert module_docs.summary == "<docstrings_test_package summary>"
    assert module_docs.details == "<docstrings_test_package details>"
    assert module_docs.deprecations == []

    assert set(module_docs.members) == {"foo", "MyEnum"}

    foo = module_docs.members["foo"]
    assert isinstance(foo, imy.docstrings.FunctionDocs)
    assert foo.owner is module_docs

    MyEnum = module_docs.members["MyEnum"]
    assert isinstance(MyEnum, imy.docstrings.ClassDocs)
    assert MyEnum.owner is module_docs
    assert set(MyEnum.members) == {
        "is_even"
    }  # The __init__ should be omitted, since it's an enum

    module_docs.add_member(docstrings_test_package.public_submodule)
    assert set(module_docs.members) == {"foo", "MyEnum", "public_submodule"}

    public_submodule = module_docs.members["public_submodule"]
    assert isinstance(public_submodule, imy.docstrings.ModuleDocs)
    assert public_submodule.object is docstrings_test_package.public_submodule
    assert public_submodule.owner is module_docs
    assert set(public_submodule.members) == {"DemoClass"}


def test_deprecated_class():
    @imy.deprecations.deprecated(since="1.1", replacement="Bar")
    class Foo:
        pass

    docs = imy.docstrings.ClassDocs.from_class(Foo)
    assert len(docs.deprecations) == 1
    assert docs.deprecations[0].since_version == "1.1"
    assert docs.deprecations[0].will_be_removed_in_version is None
    assert "Bar" in docs.deprecations[0].message


def test_deprecated_function():
    @imy.deprecations.deprecated(
        since="1.2",
        will_be_removed_in_version="1.5",
        description="It causes undefined behavior",
    )
    @imy.deprecations.parameter_renamed(
        since="1.3", old_name="old_param", new_name="param"
    )
    async def foo(param: int):
        return

    docs = imy.docstrings.FunctionDocs.from_function(foo)

    assert len(docs.deprecations) == 1
    assert docs.deprecations[0].since_version == "1.2"
    assert docs.deprecations[0].will_be_removed_in_version == "1.5"
    assert docs.deprecations[0].message == "It causes undefined behavior"
    assert not docs.synchronous
