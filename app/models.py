from pydantic import BaseModel
from sqlmodel import SQLModel, Field
import uuid 
from enum import Enum
from datetime import date, time

class Status(Enum):
    PENDING: str = "pending"
    MATCHED: str = "matched"
    REJECTED: str = "rejected"
    
class OrderType(Enum):
    BUY: str = "buy"
    SELL: str = "sell"

class Create(SQLModel):
    order_type: OrderType
    pricePerMWh: float
    quantityMW: int
    delivery_date: date
    delivery_time: time

class Bid(Create, table=True):
    bid_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    delivery_date: date
    delivery_time: time
    quantityMW: int
    pricePerMWh: float
    order_type: OrderType
    # status: Status

class ShowBid(Bid):
    pass


class Offer(Create, table=True):
    offer_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    delivery_date: date
    delivery_time: time
    quantityMW: int
    pricePerMWh: float
    order_type: OrderType
    # status: Status
  
class Update(Create):
    order_type: OrderType
    pricePerMWh: float
    quantityMW: int
    delivery_date: date
    delivery_time: time

class ShowOffer(Offer):
    pass


class Message(BaseModel):
    message: str
    id: uuid.UUID