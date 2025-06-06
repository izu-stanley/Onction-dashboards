from pydantic import BaseModel, validator
from sqlmodel import SQLModel, Field
import uuid 
from enum import Enum
from datetime import date, time,  datetime
from typing import Optional

class Status(str, Enum):
    PENDING: str = "pending"
    MATCHED: str = "matched"
    REJECTED: str = "rejected"
    APPROVED: str = "approved"
    DENIED: str = "denied"

    
class OrderType(Enum):
    BUY: str = "BUY"
    SELL: str = "SELL"


class CommonName(Enum):
    GEN_A: str = "Gen A"
    GEN_B: str = "Gen B"
    GEN_C: str = "Gen C"
    GEN_D: str = "Gen D"
    UTILITY_X: str = "Utility X"
    UTILITY_Y: str = "Utility Y"
    UTILITY_Z: str = "Utility Z"

class Create(SQLModel):
    common_name: CommonName
    trader_id:  CommonName
    order_type: OrderType
    quantity: int
    price: float
    timeslot: str = "10:00:00"
    delivery_day: date
    max_dispatch: int
    quantity_filled: int

class Order(Create, table=True):
    order_ref: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    common_name: str = CommonName
    trader_id: str = CommonName
    order_type: str = OrderType
    quantity: int
    price: float
    timeslot: str = "10:00:00"
    delivery_day: date
    fully_matched: Optional[bool] = False
    max_dispatch: int
    quantity_filled: int
    status: Optional[Status] = Status.PENDING

class Trades(SQLModel, table=True):
    id: Optional[int] = Field(default_factory=uuid.uuid4, primary_key=True)
    matching_id: uuid.UUID 
    quantity: int
    trade_id: uuid.UUID
    buyer_order_ref: uuid.UUID
    buyer_id: str
    timeslot: time
    seller_order_ref: uuid.UUID
    seller_id: str
    price: int
    created_at: datetime
    delivery_day: date

class ShowOrder(Order):
    pass

class Update(Create):
    common_name: str = CommonName
    trader_id: str= CommonName
    order_type: str = OrderType
    quantity: int
    price: float
    timeslot: str = "10:00:00"
    delivery_day: date
    fully_matched: Optional[bool] = False
    max_dispatch: int
    quantity_filled: int
    status: Status

class Message(BaseModel):
    message: str