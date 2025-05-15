from __future__ import annotations

from abc import ABC, abstractmethod
from typing import override


class RouteComponent(ABC):
    @property
    def parent(self) -> RouteComponent | None:
        return self._parent

    @parent.setter
    def parent(self, parent: RouteComponent | None) -> None:
        self._parent = parent

    def is_router(self) -> bool:
        return isinstance(self, Router)

    def add_router(self, component: RouteComponent) -> None: ...

    def remove_router(self, component: RouteComponent) -> None: ...

    @abstractmethod
    def describe(self) -> str: ...


class Endpoint(RouteComponent):
    def __init__(self, method: str, path: str) -> None:
        self.method = method
        self.path = path

    @override
    def describe(self) -> str:
        return f'Endpoint(method={self.method} path={self.path})'


class Router(RouteComponent):
    def __init__(self, prefix: str = '') -> None:
        self.prefix = prefix
        self.routes: list[RouteComponent] = []

    @override
    def add_router(self, route: RouteComponent) -> None:
        self.routes.append(route)
        route.parent = self

    @override
    def remove_router(self, route: RouteComponent) -> None:
        try:
            self.routes.remove(route)
        except ValueError:
            pass
        else:
            route.parent = None

    @override
    def describe(self) -> str:
        result = '\n'.join([str(route.describe()) for route in self.routes])

        # x = []
        # for route in self.routes:
        #     x.append(str(route.describe()))

        # result = '\n'.join(x)

        return self.prefix + '\n' + result


class Application:
    def __init__(self, name: str) -> None:
        self.name = name
        self.root_router = Router()

    def include_router(self, router: Router) -> None:
        self.root_router.add_router(router)

    def describe(self) -> None:
        print(f'Application: {self.name}')
        print(self.root_router.describe())


def client_code() -> None: ...


def main() -> None:
    app = Application('My API')

    # api
    api_router = Router(prefix='/api/v1')

    # users
    user_router = Router(prefix='/users')
    user_router.add_router(Endpoint('GET', '/get_user'))
    user_router.add_router(Endpoint('PUT', '/update_user'))
    user_router.add_router(Endpoint('DELETE', '/delete_user'))

    # books
    book_router = Router(prefix='/books')
    book_router.add_router(Endpoint('GET', '/get_book'))
    book_router.add_router(Endpoint('DELETE', '/delete_book'))

    # book authors
    book_authors = Router(prefix='/authors')
    book_authors.add_router(Endpoint('POST', '/add_book_author'))

    book_publishers = Router(prefix='/publishers')
    book_publishers.add_router(Endpoint('POST', '/add_book_publisher'))

    # -

    # /api/users
    api_router.add_router(user_router)

    # /api/books
    api_router.add_router(book_router)

    # /api/books/authors
    book_router.add_router(book_authors)
    # api/books/publishers
    book_router.add_router(book_publishers)

    # add api to app
    app.include_router(api_router)
    app.describe()


if __name__ == '__main__':
    main()
