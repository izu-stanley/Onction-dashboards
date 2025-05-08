from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated, Any, Union
from models import Create, Message, Update, ShowOrder, Order, Trades
from sqlmodel import Session
from db.db import get_db
import uuid


SessionInit = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/Genco-Dashboard", tags=["Genco Dashboard"])


@router.get("/offer/{trader_id}", response_model=List[ShowOrder])
def all_offer(*, session: SessionInit, trader_id: str) -> Any:
    try:
        offer = session.query(Order).filter(Order.trader_id == trader_id).all()
        return offer
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))



@router.get("/Trades/{Seller_id}")
def get_trades(*, session: SessionInit, seller_id: str ) -> Any:
    try:
        trade = session.query(Trades).filter(Trades.seller_id == seller_id).all()
        if not trade:
              raise HTTPException(status_code=404, detail="trade not found or has been deleted")
        return trade
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))
    

@router.post("/submit_offer", response_model=Union[Message,ShowOrder], status_code=status.HTTP_201_CREATED)
def create_offer(*, session: SessionInit, offer_in: List[Create]) -> Any:
    create_offer = []
    try:
        for offer in offer_in:
            offer = Order.model_validate(offer)
            session.add(offer)
            session.commit()
            session.refresh(offer)
        create_offer.append(offer)
        return Message(
            message="Offer submitted successfully")
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.put("/offer/{id}", response_model=Union[ShowOrder,Message], status_code=status.HTTP_200_OK)
def update_offer(*,
                 id: uuid.UUID, 
                 offer_in: Update,
                 session: SessionInit) -> Any:
    """Update an Offer."""
    try:
        offer = session.get(Order, id)
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")
        
        update_offer = offer_in.model_dump(exclude_unset=True)
        offer.sqlmodel_update(update_offer)
        session.add(offer)
        session.commit()
        session.refresh(offer)
        return Message(
                message="Offer updated successfully")
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.delete("/offer/{id}", response_model=Message, status_code=status.HTTP_200_OK)
def delete_offer(*, id: uuid.UUID,
                 session: SessionInit) -> Any:
    """Delete an Offer."""

    offer = session.get(Order, id)
    if not offer:
        raise HTTPException(status_code=404, detail="Bid not found")
    session.delete(offer)
    session.commit()
    return Message(
            message="offer deleted successfully")