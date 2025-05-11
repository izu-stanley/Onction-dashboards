from fastapi import APIRouter, Depends, status, HTTPException
from typing import  Annotated, Any
from models import Order, Trades, Message, Status
from sqlmodel import Session,  select
from db.db import get_db
from datetime import date
from modules.trigger_match import TriggerMatch

SessionInit = Annotated[Session,  Depends(get_db)]
router = APIRouter(prefix="/tradeclearing",tags=["Trade Clearing"])


@router.post("/trigger_matching_engine")
def trigger_matching_engine(session: SessionInit, date: date) ->  Any:
    try:
        params = {"clearing_date": str(date)}
        query = select(Order).where(Order.delivery_day == date)
        orders = session.exec(query).all()
        if orders is None:
            raise HTTPException(status_code=404, detail=str(error))
        
        create_trades = []
        payload = [{
                    **order.dict(exclude={"status"}), 
                    "order_ref": str(order.order_ref), 
                    "delivery_day": str(order.delivery_day), 
                    "timeslot": str(order.timeslot) 
                    }for order in orders]
        data = TriggerMatch().trigger_matching_engine(params, payload)

        if data == []:
            raise HTTPException(status_code=404, detail=str(data))
        else:
            for new_trade in data:
                new_trade = Trades.model_validate(new_trade)
                create_trades.append(new_trade)

                # Update status of the orders in the database
                buyer_ref = session.exec(select(Order).where(Order.order_ref == new_trade.buyer_order_ref)).all()
                seller_ref = session.exec(select(Order).where(Order.order_ref == new_trade.seller_order_ref)).all()
                
                matched_trade = [*buyer_ref, *seller_ref]
                for  order_status in matched_trade:
                    order_status.status = Status.MATCHED
                    order_status.fully_matched = True
                    session.add(order_status)

            session.add_all(create_trades)
            session.commit()
            for t in create_trades:
                session.refresh(t)
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
    


@router.get("/bid_offers/")
def all_bid(*, session: SessionInit) ->  Any:
    try:
        bid = session.query(Order).all()
        return bid
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))