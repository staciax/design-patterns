from __future__ import annotations

import json
import zlib
from abc import ABC, abstractmethod
from typing import Any, override

yellow = '\033[93m'
reset = '\033[0m'


def json_dump(data: dict[str, Any]) -> str:
    return json.dumps(
        data,
        ensure_ascii=False,
        allow_nan=False,
        indent=None,
        separators=(',', ':'),
    )


class Response:
    def __init__(self) -> None:
        self.content: bytes | None = None
        self.content_type: str | None = None
        self.status_code: int | None = None
        self.headers: bytes | None = None
        self.compressed: bool = False

    def render(self) -> str:
        attrs = [
            ('content', self.content),
            ('Content Type', self.content_type),
            ('Status Code', self.status_code),
            ('Headers', self.headers),
            ('Compressed', self.compressed),
        ]
        return '\n'.join('\033[35m{}\033[0m: \033[92m{!r}\033[0m'.format(*t) for t in attrs)


class ReponseBuilder(ABC):
    @property
    @abstractmethod
    def response(self) -> Response: ...

    @abstractmethod
    def build_content(self, content: Any) -> None: ...

    @abstractmethod
    def build_content_type(self, content_type: str) -> None: ...

    @abstractmethod
    def build_status_code(self, status_code: int) -> None: ...

    @abstractmethod
    def build_headers(self, headers: dict[str, Any] | None) -> None: ...

    @abstractmethod
    def compress_response(self) -> None: ...


class HTMLResponseBuilder(ReponseBuilder):
    def __init__(self) -> None:
        self._response = Response()

    def reset(self) -> None:
        self._response = Response()

    @property
    def response(self) -> Response:
        response = self._response
        self.reset()
        return response

    @override
    def build_content(self, content: str) -> None:
        self._response.content = content.encode('utf-8')

    @override
    def build_content_type(self, content_type: str) -> None:
        self._response.content_type = content_type

    @override
    def build_status_code(self, status_code: int) -> None:
        self._response.status_code = status_code

    @override
    def build_headers(self, headers: dict[str, Any] | None) -> None:
        if headers:
            self._response.headers = json_dump(headers).encode('utf-8')

    @override
    def compress_response(self) -> None:
        if self._response.content:
            self._response.content = zlib.compress(self._response.content)
            self._response.compressed = True


class JSONRequestBuilder(ReponseBuilder):
    def __init__(self) -> None:
        self._response = Response()

    def reset(self) -> None:
        self._response = Response()

    @property
    def response(self) -> Response:
        response = self._response
        self.reset()
        return response

    @override
    def build_content(self, content: dict[str, Any]) -> None:
        self._response.content = json_dump(content).encode('utf-8')

    @override
    def build_content_type(self, content_type: str) -> None:
        self._response.content_type = content_type

    @override
    def build_status_code(self, status_code: int) -> None:
        self._response.status_code = status_code

    @override
    def build_headers(self, headers: dict[str, Any] | None) -> None:
        if headers:
            self._response.headers = json_dump(headers).encode('utf-8')

    @override
    def compress_response(self) -> None:
        if self._response.content:
            self._response.content = zlib.compress(self._response.content)
            self._response.compressed = True


class ReponseBuilderDirector:
    def build_response(
        self,
        builder: ReponseBuilder,
        content: str | dict[str, Any],
        status_code: int,
        headers: dict[str, Any] | None = None,
    ) -> None:
        builder.build_content(content)
        builder.build_status_code(status_code)
        builder.build_content_type('application/json' if isinstance(content, dict) else 'html/text')
        builder.build_headers(headers)

    def build_response_with_compress(
        self,
        builder: ReponseBuilder,
        content: str | dict[str, Any],
        status_code: int,
        headers: dict[str, Any] | None = None,
    ) -> None:
        if headers is not None:
            headers.update({'Content-Encoding': 'gzip'})
        else:
            headers = {'Content-Encoding': 'gzip'}
        builder.build_content(content)
        builder.build_status_code(status_code)
        builder.build_content_type('application/json' if isinstance(content, dict) else 'html/text')
        builder.build_headers(headers)
        builder.compress_response()


def client_code(director: ReponseBuilderDirector) -> None:
    print(f'{yellow}HTML Response{reset}')

    html_builder = HTMLResponseBuilder()

    director.build_response(
        html_builder,
        content='<h1>STACiA<h1>',
        status_code=200,
    )
    html_response = html_builder.response
    print(html_response.render())

    print('-' * 20)

    print(f'{yellow}JSON Response{reset}')
    json_builder = JSONRequestBuilder()

    director.build_response(
        json_builder,
        content={'error': 'User not found'},
        status_code=400,
    )
    json_response = json_builder.response
    print(json_response.render())

    print('-' * 20)

    print(f'{yellow}JSON Response with compress zlib{reset}')
    json_builder = JSONRequestBuilder()

    director.build_response_with_compress(
        json_builder,
        content={'message': 'STACiA from zlib'},
        status_code=200,
        headers={'X-TEST': 'TEST'},
    )
    json_response = json_builder.response
    print(json_response.render())

    print('-' * 20)


def main() -> None:
    director = ReponseBuilderDirector()

    client_code(director)

    print(f'{yellow}HTML Response Without Director{reset}')

    html_builder = HTMLResponseBuilder()
    html_builder.build_content('<h3>STACiA without director</h3>')
    html_builder.build_content_type('html/text')
    html_builder.build_status_code(200)
    html_builder.build_headers({'X-WITHOUT-DIRECTOR': 'true'})
    html_response = html_builder.response

    print(html_response.render())


if __name__ == '__main__':
    main()
