from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated, Any, Union
from models import Offer, Create, Message, Update, ShowOffer, Trade, Setting
from sqlmodel import Session
from db.db import get_db
import uuid
import httpx
import os

SessionInit = Annotated[Session,  Depends(get_db)]
setting = Setting()
router = APIRouter(prefix="/Genco-Dashboard",tags=["Genco Dashboard"])

api_key = os.getenv('API_KEY')
url = f"https://onction-matching-engine-762140739532.europe-west2.run.app/docs#/default/match_v1_match_post/{api_key}"


@router.get("/get_all_trades", response_model=List[Trade])
async def get_all_trades() -> Any:
    try:
        async with httpx.AsyncClient() as client:
            trade = await client.get(url)
            all_trade = trade.json()
            return all_trade
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))
 
    

@router.get("/offer", response_model=List[ShowOffer])
def all_offer(*, session: SessionInit) -> Any:
    try:
        offer = session.query(Offer).all()
        # return Show(offers=offer)
        return offer
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))
    

@router.post("/submit_offer", response_model=Union[Message,ShowOffer], status_code=status.HTTP_201_CREATED)
def create_offer(*, session: SessionInit, offer_in: List[Create]) -> Any:
    create_offer = []

    try:
        for offer in offer_in:
            offer = Offer.model_validate(offer)
            session.add(offer)
            session.commit()
            session.refresh(offer)
        create_offer.append(offer)
        return Message(
            message="Offer submitted successfully",
            id=offer.offer_id)
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.put("/offer/{id}", response_model=Union[ShowOffer,Message], status_code=status.HTTP_200_OK)
def update_offer(*,
                 id: uuid.UUID, 
                 offer_in: Update,
                 session: SessionInit) -> Any:
    """Update an Offer."""
    try:
        offer = session.get(Offer, id)
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")
        update_offer = offer_in.model_dump(exclude_unset=True)
        offer.sqlmodel_update(update_offer)
        session.add(offer)
        session.commit()
        session.refresh(offer)
        return Message(
                message="Offer updated successfully",
                id=offer.offer_id)
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))
    


@router.delete("/offer/{id}", response_model=Message, status_code=status.HTTP_200_OK)
def delete_offer(*, id: uuid.UUID,
                 session: SessionInit) -> Any:
    """Delete an Offer."""

    offer = session.get(Offer, id)
    if not offer:
        raise HTTPException(status_code=404, detail="Bid not found")
    session.delete(offer)
    session.commit()
    return Message(
            message="offer deleted successfully",
            id=offer.offer_id)