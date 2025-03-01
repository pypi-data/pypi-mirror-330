
from .store.base import BaseStore
from .store.kv.inmemory import InMemoryStore

class Config:
    allow_private_ip: bool = False
    max_redirects: int = 5
    kv: BaseStore = InMemoryStore()