import enum


class MyEnum(enum.Enum):
    FOO = 3
    BAR = 4

    @property
    def is_even(self) -> bool:
        return self.value % 2 == 0


def foo():
    pass
