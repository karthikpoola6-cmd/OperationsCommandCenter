from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routes import incidents, alerts, metrics, shipments, detect


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Operations Command Center",
    description="Real-time operational monitoring, incident management, and analytics platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(incidents.router)
app.include_router(alerts.router)
app.include_router(metrics.router)
app.include_router(shipments.router)
app.include_router(detect.router)


@app.get("/")
def root():
    return {"message": "Operations Command Center API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}
