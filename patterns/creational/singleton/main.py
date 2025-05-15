from __future__ import annotations

from typing import Any, ClassVar, Literal


class ThemeManagerMeta(type):
    _instances: ClassVar[dict[type, ThemeManagerMeta]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> ThemeManagerMeta:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ThemeManager(metaclass=ThemeManagerMeta):
    def __init__(self) -> None:
        self._current_theme: str = 'light'

    def get_current_theme(self) -> str:
        return self._current_theme

    def set_theme(self, /, value: Literal['dark', 'light']) -> None:
        self._current_theme = value


def home_page() -> None:
    t = ThemeManager()
    print('home page')
    print('theme:', t.get_current_theme())
    print('-' * 10)


def member_page() -> None:
    t = ThemeManager()
    print('member page')
    print('theme:', t.get_current_theme())
    print('-' * 10)


def main() -> None:
    t1 = ThemeManager()
    t2 = ThemeManager()

    if id(t1) == id(t2):
        print('Singleton works.')
    else:
        print('Singleton failed.')

    t1.set_theme('dark')

    print('t2 theme:', t1.get_current_theme())

    # -

    print('-' * 20)

    home_page()

    member_page()


if __name__ == '__main__':
    main()
