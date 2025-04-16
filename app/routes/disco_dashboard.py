from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated, Any, Union
from models import  Create, Bid, Message, Update, ShowBid
from sqlmodel import Session
from db.db import get_db
import uuid

SessionInit = Annotated[Session,  Depends(get_db)]
router = APIRouter(prefix="/Disco-Dashboard",tags=["Disco Dashboard"])


@router.get("/bid", response_model=List[ShowBid])
def all_bid(*, session: SessionInit) ->  Any:
    try:
        bid = session.query(Bid).all()
        return bid
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.post("/create_bid", response_model=Union[ShowBid,Message], status_code=status.HTTP_201_CREATED)
def create_bid(*, session: SessionInit, bid_in: List[Create]) -> Any:
    create_bid = []

    try:
        for bid in bid_in:
            bid = Bid.model_validate(bid)
            session.add(bid)
            session.commit()
            session.refresh(bid)
        create_bid.append(bid)
        return Message(
            message="bid submitted successfully",
            id=bid.bid_id)
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.put("/update_bid/{id}", response_model=Union[ShowBid,Message], status_code=status.HTTP_200_OK)
def update_bid(*,
                 id: uuid.UUID, 
                 bid_in: Update,
                 session: SessionInit) -> Any:
    """Update a Bid."""
    try:
        bid = session.get(Bid, id)
        if not bid:
            raise HTTPException(status_code=404, detail="Order not found")
        update_bid = bid_in.model_dump(exclude_unset=True)
        bid.sqlmodel_update(update_bid)
        session.add(bid)
        session.commit()
        session.refresh(bid)
        return Message(
                message="Order updated successfully",
                id=bid.bid_id)
    
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.delete("/delete_bid/{id}", response_model=Message, status_code=status.HTTP_200_OK)
def delete_bid(*, id: uuid.UUID,
                 session: SessionInit) -> Any:
    """
    Delete an Order.
    """
    bid = session.get(Bid, id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    session.delete(bid)
    session.commit()
    return Message(
            message="Bid deleted successfully",
            id=bid.bid_id)