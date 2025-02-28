from collections.abc import Callable
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class MockRoute:
    message_type: str
    func_call: Callable | None = None

    def __call__(self, func_call: Callable) -> None:
        self.func_call = func_call


class MockHandler:
    routes: ClassVar = {}

    def route(self, message_type: str) -> MockRoute:
        route = MockRoute(message_type=message_type)
        self.routes[message_type] = route
        return route

    def assert_has_route(self, message_type: str, func_call: Callable) -> None:
        assert message_type in self.routes
        assert self.routes[message_type].func_call == func_call

    @property
    def route_count(self) -> int:
        return len(self.routes)

    def assert_has_only_routes(self, routes: list[tuple[str, Callable]]) -> None:
        assert len(routes) == self.route_count
        for message_type, func_call in routes:
            self.assert_has_route(message_type, func_call)
