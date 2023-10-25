from pydantic import BaseModel


class Currency(BaseModel):
    symbol: str
    price: float
