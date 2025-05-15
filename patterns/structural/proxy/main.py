import itertools
from abc import ABC, abstractmethod


class IServer(ABC):
    @abstractmethod
    def handle_request(self, request: str) -> None: ...


class Server(IServer):
    def __init__(self, name: str) -> None:
        self.name = name

    def handle_request(self, request: str) -> None:
        print(f'{self.name} processing {request}')


class LoadBalancerProxy(IServer):
    def __init__(self, servers: list[Server]) -> None:
        self.servers = itertools.cycle(servers)

    def handle_request(self, request: str) -> None:
        server = next(self.servers)
        server.handle_request(request)


def client() -> None:
    servers = [
        Server('backend-01'),
        Server('backend-02'),
    ]

    lb = LoadBalancerProxy(servers)

    lb.handle_request('request 1')
    lb.handle_request('request 2')
    lb.handle_request('request 3')
    lb.handle_request('request 4')
    lb.handle_request('request 5')
    lb.handle_request('request 6')


def main() -> None:
    client()


main()
