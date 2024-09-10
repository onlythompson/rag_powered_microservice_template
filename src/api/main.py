from fastapi import FastAPI, Request
from src.api.routes import ingest, query, index, conversation
from src.core.config import settings
from src.core.observability import instrument_app, track_requests

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Instrument the FastAPI app for observability
instrument_app(app)

# Add middleware for request tracking
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    return await track_requests(request, call_next)

app.include_router(ingest.router, prefix="/api/v1", tags=["ingestion"])
app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(index.router, prefix="/api/v1", tags=["index"])
app.include_router(conversation.router, prefix="/api/v1", tags=["conversation"])

@app.get("/")
async def root():
    return {"message": "Welcome to the {settings.PROJECT_NAME}", "version": settings.VERSION}