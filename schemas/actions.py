from typing import List

from pydantic import BaseModel


class Subscribe(BaseModel):
    action: str = 'subscribe'
    symbols: List[str]


class Unsubscribe(BaseModel):
    action: str = 'unsubscribe'
    symbols: List[str]