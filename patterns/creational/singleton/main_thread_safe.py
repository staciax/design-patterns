from __future__ import annotations

from threading import Lock, Thread
from typing import Any, ClassVar, Literal


class ThemeManagerMeta(type):
    _instances: ClassVar[dict[type, ThemeManagerMeta]] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> ThemeManagerMeta:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class ThemeManager(metaclass=ThemeManagerMeta):
    def __init__(self, default_theme: Literal['dark', 'light'] = 'light') -> None:
        self._current_theme: str = default_theme

    def get_current_theme(self) -> str:
        return self._current_theme

    def set_theme(self, /, value: Literal['dark', 'light']) -> None:
        self._current_theme = value


def home_page(default_theme: Literal['dark', 'light']) -> None:
    t = ThemeManager(default_theme)
    print('home page')
    print('theme:', t.get_current_theme())
    print('-' * 10)


def member_page(default_theme: Literal['dark', 'light']) -> None:
    t = ThemeManager(default_theme)
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

    process1 = Thread(target=home_page, args=('dark',))
    process2 = Thread(target=member_page, args=('light',))

    process1.start()
    process2.start()


if __name__ == '__main__':
    main()
