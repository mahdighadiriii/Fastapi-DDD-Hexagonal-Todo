from typing import Dict, List, Type

from application.interfaces.event_bus import EventBus, EventHandler
from domain.events.base import DomainEvent


class InMemoryEventBus(EventBus):
    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[EventHandler]] = {}

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def publish(self, event: DomainEvent) -> None:
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                await handler(event)
