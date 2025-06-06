from datetime import datetime, timedelta, time
import random
from typing import Any, List


class Marketdata():
    def __init__(self):
        pass

    def generate_market_data(self, data) -> List[Any]:
        data = []
        start_time = datetime.utcnow()
        for i in range(24):
            data.append({
                "timestamp": (start_time + timedelta(hours=i)).isoformat(),
                "pricePerMWh": round(random.randint(4000, 6000), 2),
                "totalDemandMWh": random.randint(10000, 15000),
                "totalSupplyMWh": random.randint(9000, 14000)
            })
        return data