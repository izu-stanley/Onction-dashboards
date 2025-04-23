from fastapi import APIRouter, Depends, status, HTTPException
from typing import  Annotated, Any
from models import Order, Trades, Message
from sqlmodel import Session,  select
from db.db import get_db
from config import settings
import requests
from datetime import date
import os 


SessionInit = Annotated[Session,  Depends(get_db)]
router = APIRouter(prefix="/tradeclearing",tags=["Trade Clearing"])

url = f"https://onction-matching-engine-762140739532.europe-west2.run.app/v1/match"
api_key = os.getenv('api-key')

@router.post("/trigger_matching_engine")
def trigger_matching_engine(session: SessionInit, date: date) ->  Any:
    try:
        params = {"clearing_date": str(date)}
        headers = {
            "accept": "application/json",
            "X-API-Key": f"{api_key}",
            "Content-Type": "application/json",
        }  
        query = select(Order).where(Order.delivery_day == date)
        orders = session.exec(query).all()
        if query is None:
            raise HTTPException(status_code=404, detail=str(error))
        else:
          create_trades = []
          trade = requests.post(url,
                                headers=headers,
                                params=params, 
                                json=[{
                                      **order.dict(), 
                                       "order_ref": str(order.order_ref), 
                                       "delivery_day": str(order.delivery_day), 
                                       "timeslot": str(order.timeslot) 
                                       }for order in orders])
        for new_trade in trade.json():
            new_trade = Trades.model_validate(new_trade)
            session.add(new_trade)
            session.commit()
            session.refresh(new_trade)
        create_trades.append(new_trade)
        return create_trades
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))
  
    
@router.get("/get_all_trades")
def get_trades(*, session: SessionInit) -> Any:
    try:
        trade = session.query(Trades).all()
        return trade
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))
    

@router.get("/get_trades/{id}")
def get_trades(*, session: SessionInit,
                buyer_id: str,
                seller_id: str ) -> Any:
    try:
        # trade = session.query(Trades).filter(Trades.id == id).first()
        trade = session.query(Trades).filter(Trades.buyer_id == buyer_id,
                                             Trades.seller_id == seller_id).first()
        if not trade:
              raise HTTPException(status_code=404, detail="trade not found or has been deleted")
        return trade
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.delete("delete_trade/{id}", response_model=Message)
def delete_trade(*, session: SessionInit, id: int) -> Any:
    try:
        trade = session.query(Trades).filter(Trades.id == id).first()
        if not trade:
              raise HTTPException(status_code=404, detail="trade not found")
        session.delete(trade)
        session.commit()
        return Message(
            message="Trade deleted successfully"
            )
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))
