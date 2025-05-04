from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated, Any, Union
from models import  Create, Order, Message, Update, ShowOrder, Trades
from sqlmodel import Session
from db.db import get_db
import uuid

SessionInit = Annotated[Session,  Depends(get_db)]
router = APIRouter(prefix="/Disco-Dashboard",tags=["Disco Dashboard"])


@router.get("/bid", response_model=List[ShowOrder])
def all_bid(*, session: SessionInit) ->  Any:
    try:
        bid = session.query(Order).all()
        return bid
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.get("/Trades/{Buyer_id}")
def get_trades(*, session: SessionInit, buyer_id: str ) -> Any:
    try:
        trade = session.query(Trades).filter(Trades.buyer_id == buyer_id).all()
        if not trade:
              raise HTTPException(status_code=404, detail="trade not found or has been deleted")
        return trade
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))
    


@router.post("/create_bid", response_model=Union[ShowOrder,Message], status_code=status.HTTP_201_CREATED)
def create_bid(*, session: SessionInit, bid_in: List[Create]) -> Any:
    create_bid = []
    try:
        for bid in bid_in:
            bid = Order.model_validate(bid)
            session.add(bid)
            session.commit()
            session.refresh(bid)
        create_bid.append(bid)
        return Message(
            message="bid submitted successfully")
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.put("/update_bid/{id}", response_model=Union[ShowOrder,Message], status_code=status.HTTP_200_OK)
def update_bid(*,
                 id: uuid.UUID, 
                 bid_in: Update,
                 session: SessionInit) -> Any:
    """Update a Bid."""
    try:
        bid = session.get(Order, id)
        if not bid:
            raise HTTPException(status_code=404, detail="Order not found")
        update_bid = bid_in.model_dump(exclude_unset=True)
        bid.sqlmodel_update(update_bid)
        session.add(bid)
        session.commit()
        session.refresh(bid)
        return Message(
                message="Bid updated successfully")
    
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.delete("/delete_bid/{id}", response_model=Message, status_code=status.HTTP_200_OK)
def delete_bid(*, id: uuid.UUID,
                 session: SessionInit) -> Any:
    """
    Delete an Order.
    """
    bid = session.get(Order, id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    session.delete(bid)
    session.commit()
    return Message(
            message="Bid deleted successfully")