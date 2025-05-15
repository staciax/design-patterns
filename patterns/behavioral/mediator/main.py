from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod
from typing import Any


class ServiceMediator(ABC):
    @abstractmethod
    def send_request(
        self,
        sender: Microservice,
        service_name: str,
        event: str,
        data: dict[str, Any],
    ) -> None: ...


class APIGateway(ServiceMediator):
    def __init__(self) -> None:
        self._services: dict[str, Microservice] = {}

    def register_service(self, service: Microservice) -> None:
        self._services[service.name] = service
        service.set_mediator(self)

    def send_request(
        self,
        sender: Microservice,
        service_name: str,
        event: str,
        data: dict[str, Any],
    ) -> None:
        if service_name in self._services:
            print(f'API Gateway routing request from {sender.name} to {service_name}')
            service = self._services[service_name]
            service.handle_request(event, data)
        else:
            print(f'Service {service_name} not found')


class Microservice:
    def __init__(self, name: str, mediator: ServiceMediator | None = None) -> None:
        self.name = name
        self._mediator = mediator

    def set_mediator(self, mediator: ServiceMediator) -> None:
        self._mediator = mediator

    def send(self, service_name: str, event: str, data: dict[str, Any]) -> None:
        if self._mediator:
            self._mediator.send_request(self, service_name, event, data)

    @abstractmethod
    def handle_request(self, event: str, data: dict[str, Any]) -> None: ...


@dataclasses.dataclass
class Product:
    id: str
    quantity: int


class ProductService(Microservice):
    def __init__(self, name: str, mediator: ServiceMediator | None = None) -> None:
        super().__init__(name, mediator)
        self.inventory = {
            '1': Product('1', 10),
            '2': Product('2', 5),
            '3': Product('3', 0),
        }

    def handle_request(self, event: str, data: dict[str, Any]) -> None:
        if event == 'check_inventory':
            order_id = data['order_id']
            product_id = data['product_id']
            quantity = data['quantity']

            print(f'{self.name} checking inventory for product {product_id}')

            available = product_id in self.inventory and self.inventory[product_id].quantity >= quantity

            payload = {
                'order_id': order_id,
                'product_id': product_id,
                'quantity': quantity,
                'available': available,
            }

            self.send('order_service', 'inventory_result', payload)


@dataclasses.dataclass
class Order:
    id: str
    product_id: str
    quantity: int


class OrderService(Microservice):
    def __init__(self, name: str, mediator: ServiceMediator | None = None) -> None:
        super().__init__(name, mediator)
        self.orders: dict[str, Order] = {}

    def create_order(self, data: dict[str, Any]) -> None:
        payload = {
            'order_id': data['order_id'],
            'product_id': data['product_id'],
            'quantity': data['quantity'],
        }
        self.send('product_service', 'check_inventory', payload)

    def handle_request(self, event: str, data: dict[str, Any]) -> None:
        if event == 'inventory_result':
            if data.get('available'):
                order = Order(data['order_id'], data['product_id'], data['quantity'])
                self.orders[order.id] = order
                print(f'{self.name} created order {order}')
            else:
                print(f'{self.name} cancelling order {data["order_id"]}')


if __name__ == '__main__':
    gateway = APIGateway()

    product_service = ProductService('product_service')
    order_service = OrderService('order_service')

    gateway.register_service(order_service)
    gateway.register_service(product_service)

    order_service.create_order({
        'order_id': '5',
        'product_id': '1',
        'quantity': 5,
    })

    print('-' * 30)

    order_service.create_order({
        'order_id': '7',
        'product_id': '2',
        'quantity': 10,
    })
