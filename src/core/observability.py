# src/core/observability.py

import time
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import Counter, Histogram, Gauge
import logging
from pythonjsonlogger import jsonlogger
from src.core.config import settings

# Initialize OpenTelemetry
resource = Resource(attributes={
    "service.name": "rag-microservice",
    "environment": settings.ENVIRONMENT
})

trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint=settings.OTLP_ENDPOINT)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

# Initialize Prometheus metrics
REQUESTS_TOTAL = Counter(
    'requests_total', 'Total number of requests', ['method', 'endpoint', 'http_status']
)
REQUEST_DURATION = Histogram(
    'request_duration_seconds', 'Request duration in seconds', ['method', 'endpoint']
)
DOCUMENTS_PROCESSED = Counter('documents_processed_total', 'Total number of documents processed')
EMBEDDING_GENERATION_DURATION = Histogram(
    'embedding_generation_duration_seconds', 'Embedding generation duration in seconds'
)
LLM_QUERY_DURATION = Histogram('llm_query_duration_seconds', 'LLM query duration in seconds')
VECTOR_STORE_QUERY_DURATION = Histogram(
    'vector_store_query_duration_seconds', 'Vector store query duration in seconds'
)
ACTIVE_REQUESTS = Gauge('active_requests', 'Number of active requests')

# Configure JSON logging
logger = logging.getLogger("rag_microservice")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Middleware for request tracking
async def track_requests(request, call_next):
    ACTIVE_REQUESTS.inc()
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    ACTIVE_REQUESTS.dec()
    
    REQUESTS_TOTAL.labels(method=request.method, endpoint=request.url.path, http_status=response.status_code).inc()
    REQUEST_DURATION.labels(method=request.method, endpoint=request.url.path).observe(duration)
    
    return response

# Decorator for tracing and metrics
def trace_and_measure(name):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(name):
                start_time = time.time()
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                
                if name == "process_document":
                    DOCUMENTS_PROCESSED.inc()
                elif name == "generate_embedding":
                    EMBEDDING_GENERATION_DURATION.observe(duration)
                elif name == "llm_query":
                    LLM_QUERY_DURATION.observe(duration)
                elif name == "vector_store_query":
                    VECTOR_STORE_QUERY_DURATION.observe(duration)
                
                return result
        return wrapper
    return decorator

# Function to instrument FastAPI
def instrument_app(app):
    FastAPIInstrumentor.instrument_app(app)

# src/core/config.py (update)

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ... (existing settings)
    
    # Observability settings
    ENVIRONMENT: str = "production"
    OTLP_ENDPOINT: str = "http://otel-collector:4317"
    LOG_LEVEL: str = "INFO"

    # ... (rest of the settings)

    class Config:
        env_file = ".env"

settings = Settings()

# Example usage in src/api/main.py

from fastapi import FastAPI, Request
from src.core.observability import instrument_app, track_requests, logger

app = FastAPI()

# Instrument the FastAPI app
instrument_app(app)

# Add middleware for request tracking
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    return await track_requests(request, call_next)

# Example route with logging
@app.get("/")
async def root():
    logger.info("Root endpoint accessed", extra={"user_agent": request.headers.get("user-agent")})
    return {"message": "Welcome to the RAG-Enabled LLM Microservice"}

# Example of using the trace_and_measure decorator
from src.core.observability import trace_and_measure

@app.post("/process_document")
@trace_and_measure("process_document")
async def process_document(document: Document):
    # Process document
    pass

@app.post("/query")
@trace_and_measure("llm_query")
async def query(query: Query):
    # Perform LLM query
    pass