from abc import ABC, abstractmethod
from typing import Any, Callable, Type

from src.domain.events.base import DomainEvent

EventHandler = Callable[[DomainEvent], Any]


class EventBus(ABC):
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        pass

    @abstractmethod
    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        pass
