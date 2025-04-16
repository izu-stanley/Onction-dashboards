from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated, Any, Union
from models import *
from sqlmodel import Session
from db.db import get_db
import uuid

SessionInit = Annotated[Session,  Depends(get_db)]
router = APIRouter(prefix="/tradeclearing",tags=["Trade Clearing"])

@router.get("/getalltrades")
def all_trades():
    pass