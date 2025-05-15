from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Self


class Request:
    def __init__(
        self,
        method: str,
        url: str,
        body: str | dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        self.method = method
        self.url = url
        self.body = body
        self.headers = headers

    def __repr__(self) -> str:
        return f'Request(method={self.method}, url={self.url})'


class RequestHandler(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.next_handler: RequestHandler | None = None

    def set_next_handler(self, handler: RequestHandler) -> Self:
        self.next_handler = handler
        return self

    @abstractmethod
    def handle(self, r: Request) -> Request: ...


class Middleware(RequestHandler):
    def handle(self, r: Request) -> Request:
        if self.next_handler:
            self.next_handler.handle(r)
        return r


class CORSMiddleWare(Middleware):
    def __init__(self, allowed_origins: list[str]) -> None:
        super().__init__()
        self.allowed_origins = allowed_origins

    def handle(self, r: Request) -> Request:
        # print('cors middleware')

        if self.allowed_origins == ['*']:
            return super().handle(r)

        if not r.headers:
            raise ValueError('CORS Error missing headers')

        origin = r.headers.get('origin')

        if origin not in self.allowed_origins:
            raise ValueError('CORS Error origin not allowed')

        return super().handle(r)


class ValidationMiddleWare(Middleware):
    def handle(self, r: Request) -> Request:
        # print('validate middleware')

        if r.method == 'POST' and r.headers:
            content_type = r.headers.get('content-type')
            if content_type == 'aplication/json' and not isinstance(r.body, dict):
                raise ValueError('Invalid Body')

        return super().handle(r)


class AuthenticationMiddleWare(Middleware):
    def handle(self, r: Request) -> Request:
        # print('auth middleware')

        if not r.headers:
            raise ValueError('Unauthorize')

        token = r.headers.get('Authorization')
        if not token:
            raise ValueError('Unauthorize')

        token_is_valid = bool(token)
        if not token_is_valid:
            raise ValueError('Invalid Token')

        return super().handle(r)


def client(middleware_handler: RequestHandler) -> None:
    request = Request(
        method='GET',
        url='localhost:3000/api/users',
        headers={
            'origin': 'localhost:8000',
            'Authorization': 'Bereer my-token',
        },
    )

    allowed_request = middleware_handler.handle(request)

    print(f'allowed_request: {allowed_request}')


def client2(middleware_handler: RequestHandler) -> None:
    # frontend
    request = Request(
        method='POST',
        body='string-body',
        url='localhost:3000/api/users',
        headers={
            'origin': 'localhost:8000',
            'Authorization': 'Bereer my-token',
            'content-type': 'aplication/json',
        },
    )

    # backend

    allowed_request = middleware_handler.handle(request)

    print(f'allowed_request: {allowed_request}')


def main() -> None:
    cors = CORSMiddleWare(['*'])
    validate = ValidationMiddleWare()
    auth = AuthenticationMiddleWare()

    cors.set_next_handler(validate)
    validate.set_next_handler(auth)

    client(cors)

    # client2(cors)


main()
