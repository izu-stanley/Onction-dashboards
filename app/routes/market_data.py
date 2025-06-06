from fastapi import APIRouter
from modules.market_data  import Marketdata

router = APIRouter(prefix="/market-data",tags=["market data"])

@router.get("/")
def get_market_data():
    return Marketdata().generate_market_data([])