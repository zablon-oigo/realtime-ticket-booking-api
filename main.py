from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.core  import initdb
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initdb() 
    yield

app = FastAPI(
    title="Tickets Booking API",
    description="A RealTime Ticket Booking RESTful API",
    lifespan=lifespan
)

@app.get("/")
def home():
    return {"msg": "Hello, World!"}
