from abc import ABC, abstractmethod
from utils.Registry import Registry
from utils import EventBus, BaseEvent

class RoleEvent(BaseEvent):
    def __init__(self,)

class BaseRole(ABC):
    
    def __init__(self, hidden=True):
        self.hidden = hidden
        


