from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated, Any, Union
from models import Bid, Offer
from sqlmodel import Session
from db.db import get_db
import uuid

SessionInit = Annotated[Session,  Depends(get_db)]
router = APIRouter(prefix="/tradeclearing",tags=["Trade Clearing"])

@router.get("/getalltrades", status_code=status.HTTP_200_OK)
def all_trades(*, session: SessionInit) ->  Any:

    try:
        items = session.query(Bid).all()
        return items
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))