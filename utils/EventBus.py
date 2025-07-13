from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import Callable, Dict, List, Any
import asyncio
from collections import defaultdict
from typing import Type

@dataclass
class BaseEvent(ABC):
    sender: object
    meta: dict[str, object] = field(default_factory=dict,kw_only=True) 
    
    def __post_init__(self):
        self.timestamp: datetime = field(default_factory=datetime.now, init=False)
        self.event_id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    
    

class EventBus:
    
    def __init__(self):
        self.subscriptions: Dict[BaseEvent,List[Callable[..., Any]]] = defaultdict(list)
        
    def on(self,event_types: list[Type[BaseEvent]] | Type[BaseEvent]):
        if event_types is not Type[list]:
                event_types = [event_types]
        def decorator(function):
            for type in event_types:
                self.subscriptions[type].append(function)
            return function
        return decorator
        
    async def post(self, event: BaseEvent):
        for function in self.subscriptions.get(type(event),[]):
            result = function(event)
            if asyncio.iscoroutine(result):
                await result
              
    def sync_post(self, event: BaseEvent):
        asyncio.run(self.post(event))
        