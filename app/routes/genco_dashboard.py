from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated, Any, Union
from models import Create, Message, Update, ShowOrder, Order
from sqlmodel import Session, select
from db.db import get_db
import uuid
from datetime import date
import json

SessionInit = Annotated[Session,  Depends(get_db)]

router = APIRouter(prefix="/Genco-Dashboard",tags=["Genco Dashboard"])


@router.get("/offer", response_model=List[ShowOrder])
def all_offer(*, session: SessionInit, date: date) -> Any:
    try:
        # offer = session.query(Order).all()
        query = select(Order).where(Order.delivery_day == str(date))
        query = session.exec(query).all()
        return query
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
            message="Offer submitted successfully",
            id=offer.order_ref)
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
                message="Offer updated successfully",
                id=offer.order_ref)
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
            message="offer deleted successfully",
            id=offer.order_ref)