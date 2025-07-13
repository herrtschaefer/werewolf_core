from typing import TypeVar, Generic, DefaultDict
T = TypeVar('T')


class Registry(Generic[T]):

    def __init__(self):
        self.items: dict[str, T] = {}
      
    def register(self, key, item: T, override=False) -> None:
      
        if key in self.items and not override:
            raise ValueError(f"Item {item} already registered. Use override=True to override an item")
        else:
            self.items[key] = item
         
    def unregister(self, key) -> None:
        if key not in self.items:
            raise KeyError("Item is not in registry.")
        else:
            del self.items[key]
          
    def has(self, key) -> bool:
        return key in self.items
 
    def get(self, key, default: T) -> T:
        return self.items.get(key, default)
  
    def all(self):
        return self.items
  
    def clear(self):
        self.items.clear()
        
    def __len__(self):
        return self.items.__len__()
    
    def __str__(self):
        return "<" + ", ".join(f"'{k}': '{v}'" for k, v in self.items.items()) + ">"
            
