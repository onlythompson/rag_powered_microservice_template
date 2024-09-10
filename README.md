# RAG-Enabled LLM Microservice

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
   - [API Endpoints](#api-endpoints)
   - [Using Agents](#using-agents)
   - [Using Chains](#using-chains)
   - [Document Ingestion](#document-ingestion)
   - [Querying](#querying)
   - [Conversation Management](#conversation-management)
7. [Observability](#observability)
8. [Development](#development)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Contributing](#contributing)
12. [License](#license)

## Introduction

This project is a production-grade RAG-enabled (Retrieval-Augmented Generation) LLM (Large Language Model) microservice. It combines the power of vector databases, language models, and advanced RAG techniques to provide sophisticated question-answering capabilities. The system is designed to be scalable, observable, and easily extensible.

## Features

- RAG-based question answering
- Multiple agent types for different tasks
- Flexible chain system for various text processing tasks
- Document ingestion and management
- Conversation context management
- Comprehensive observability with OpenTelemetry
- Asynchronous API built with FastAPI
- Easy integration with various LLMs and vector stores
- Extensible architecture for adding new capabilities

## Architecture

The microservice is built using a modular architecture with the following main components:

- **API Layer**: FastAPI-based REST API
- **Agents**: Intelligent agents for complex tasks
- **Chains**: Reusable processing pipelines
- **Services**: Core business logic
- **Data Layer**: Document loaders and data connectors
- **Vector Stores**: For efficient similarity search
- **LLMs**: Integration with language models
- **Observability**: Comprehensive tracing and monitoring

The system follows clean architecture principles, separating concerns and allowing for easy testing and maintenance.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-repo/rag-microservice.git
   cd rag-microservice
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install OpenTelemetry and related packages:
   ```
   pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi opentelemetry-exporter-otlp
   pip install prometheus-client
   pip install python-json-logger
   ```

## Configuration

1. Copy the example environment file:
   ```
   cp .env.example .env
   ```

2. Edit the `.env` file with your specific configuration:
   ```
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment
   PINECONE_INDEX_NAME=your_pinecone_index_name
   LLM_MODEL_NAME=gpt-3.5-turbo
   VECTOR_STORE_TYPE=pinecone
   OTLP_ENDPOINT=http://localhost:4317
   ```

## Usage

### API Endpoints

Start the FastAPI server:

```
uvicorn src.api.main:app --reload
```

The API will be available at `http://localhost:8000`. You can access the OpenAPI documentation at `http://localhost:8000/docs`.

### Using Agents

Agents are intelligent entities that can perform complex tasks. Here's an example of using the RAG agent via the API:

```http
POST /api/v1/agent/run
Content-Type: application/json

{
  "agent_type": "rag",
  "params": {
    "query": "What is the capital of France?"
  }
}
```

Response:
```json
{
  "result": "The capital of France is Paris. Paris is the largest city in France and serves as the country's political, economic, and cultural center. It is known for its iconic landmarks such as the Eiffel Tower, the Louvre Museum, and Notre-Dame Cathedral."
}
```

### Using Chains

Chains are reusable processing pipelines. Here's an example of using the summarization chain:

```http
POST /api/v1/chain/run
Content-Type: application/json

{
  "chain_type": "summarization",
  "inputs": {
    "text": "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals."
  }
}
```

Response:
```json
{
  "result": {
    "summary": "Artificial intelligence (AI) is machine-demonstrated intelligence, contrasting with natural intelligence in animals and humans. AI research focuses on studying intelligent agents that perceive their environment and act to achieve goals."
  }
}
```

### Document Ingestion

To ingest a document into the system:

```http
POST /api/v1/ingest/file
Content-Type: multipart/form-data

file=@path/to/your/document.pdf
```

Response:
```json
{
  "message": "Ingested file: document.pdf",
  "document_count": 5
}
```

### Querying

To query the RAG system:

```http
POST /api/v1/query
Content-Type: application/json

{
  "query": "What are the main types of machine learning?",
  "conversation_id": "user123"
}
```

Response:
```json
{
  "query": "What are the main types of machine learning?",
  "answer": "The main types of machine learning are:\n\n1. Supervised Learning: The algorithm learns from labeled data to make predictions or decisions.\n\n2. Unsupervised Learning: The algorithm finds patterns in unlabeled data.\n\n3. Reinforcement Learning: The algorithm learns through interaction with an environment, receiving feedback in the form of rewards or penalties.\n\n4. Semi-Supervised Learning: A combination of supervised and unsupervised learning, using both labeled and unlabeled data.\n\n5. Deep Learning: A subset of machine learning based on artificial neural networks with multiple layers.",
  "source_documents": [
    {"content": "Machine learning types include supervised, unsupervised, and reinforcement learning.", "metadata": {"source": "ML_textbook.pdf"}},
    {"content": "Deep learning is a subset of machine learning based on artificial neural networks.", "metadata": {"source": "AI_overview.pdf"}}
  ]
}
```

### Conversation Management

To manage a conversation:

```http
POST /api/v1/conversation/message
Content-Type: application/json

{
  "conversation_id": "user123",
  "message": "Tell me more about supervised learning."
}
```

Response:
```json
{
  "response": "Supervised learning is a type of machine learning where the algorithm learns from labeled data. In this approach, the algorithm is trained on a dataset where the correct answers (labels) are provided. The goal is for the algorithm to learn the relationship between the input data and the labels, so it can make accurate predictions on new, unseen data. Common applications of supervised learning include classification (predicting a category) and regression (predicting a continuous value).",
  "summary": "The conversation covered an introduction to machine learning types, with a focus on supervised learning. Supervised learning was explained as a method where algorithms learn from labeled data to make predictions on new data."
}
```

## Observability

This microservice is instrumented with OpenTelemetry for comprehensive observability. Here's how to access the observability features:

1. Metrics: Available at `http://localhost:8000/metrics`
2. Traces: Sent to the configured OTLP endpoint (default: `http://localhost:4317`)
3. Logs: JSON-formatted logs are output to stdout and can be collected by your logging infrastructure

Example of accessing metrics:

```bash
curl http://localhost:8000/metrics
```

This will return Prometheus-formatted metrics, including custom metrics like `documents_processed_total` and `embedding_generation_duration_seconds`.

## Development

To set up the development environment:

1. Install development dependencies:
   ```
   pip install -r requirements-dev.txt
   ```

2. Set up pre-commit hooks:
   ```
   pre-commit install
   ```

3. Run tests:
   ```
   pytest
   ```

4. Check code style:
   ```
   flake8 src tests
   black src tests --check
   isort src tests --check-only
   ```

## Testing

Run the test suite:

```
pytest
```

For coverage report:

```
pytest --cov=src --cov-report=html
```

## Deployment

This microservice can be deployed using Docker. A `Dockerfile` is provided in the repository.

1. Build the Docker image:
   ```
   docker build -t rag-microservice .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 --env-file .env rag-microservice
   ```

For production deployment, consider using Kubernetes for orchestration and scaling.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.