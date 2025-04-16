from fastapi import FastAPI
from routes import system_operator, genco_dashboard, disco_dashboard
from db.db import create_db_and_tables

app = FastAPI(title="Onction Disco dashboard", version="1.0.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(system_operator.router)
app.include_router(genco_dashboard.router)
app.include_router(disco_dashboard.router)