from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.core  import initdb
from src.auth.routes import auth_router

app = FastAPI()
version = 'v1'
@asynccontextmanager
async def lifespan(app: FastAPI):
    await initdb() 
    yield

app = FastAPI(
    title="Tickets Booking API",
    description="A RealTime Ticket Booking RESTful API",
    lifespan=lifespan,
    version=version
)
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
@app.get("/")
def home():
    return {"msg": "Hello, World!"}
