import pytest
from utils.EventBus import BaseEvent, EventBus
from dataclasses import dataclass
import asyncio
@pytest.fixture
def Bus():
    return EventBus()

def test_register_Callback(Bus):
    called = []
    
    @Bus.on(BaseEvent)
    def handler(event):
        called.append("OK")
    
    assert handler in Bus.subscriptions[BaseEvent]
    event = BaseEvent(sender=test_register_Callback)
    Bus.sync_post(event)
    assert called == ["OK"]

@dataclass
class CustomEvent(BaseEvent):
    custom_data: str
      
def test_Subscribe_toCustom_event(Bus):
    
    called = []
    
    @Bus.on(CustomEvent)
    def handler(event):
        called.append(event.custom_data)
    
    assert handler in Bus.subscriptions[CustomEvent]
    event = CustomEvent(sender=test_Subscribe_toCustom_event, custom_data="OK")
    event2 = BaseEvent(sender=test_Subscribe_toCustom_event)
    Bus.sync_post(event)
    Bus.sync_post(event2)
    assert called == ["OK"] and len(called) == 1
    
def test_No_interaction_toCustom_event(Bus):
    
    called = []
    
    @Bus.on(BaseEvent)
    def handler(event):
        called.append(type(event))
    
    assert handler in Bus.subscriptions[BaseEvent]
    event = CustomEvent(sender=test_Subscribe_toCustom_event, custom_data="OK")
    event2 = BaseEvent(sender=test_Subscribe_toCustom_event)
    Bus.sync_post(event)
    Bus.sync_post(event2)
    assert called == [BaseEvent] and len(called) == 1


@pytest.mark.asyncio
async def test_async_handler_is_called(Bus):
   
    called = []

    @Bus.on(BaseEvent)
    async def handler(event):
        await asyncio.sleep(0.01)
        called.append(event.sender)

    await Bus.post(BaseEvent(sender="ok"))
    assert called == ["ok"]  

@pytest.mark.asyncio
async def test_handler_timeout(Bus):
    

    @Bus.on(BaseEvent)
    async def slow_handler(event):
        await asyncio.sleep(2)  # 2 Sekunden Verzögerung

    # asyncio.wait_for erzeugt den Timeout
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(Bus.post(BaseEvent(sender="x")), timeout=0.1)