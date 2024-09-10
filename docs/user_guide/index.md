# RAG-Enabled LLM Microservice User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
   - [System Requirements](#system-requirements)
   - [Installation](#installation)
   - [Configuration](#configuration)
3. [Authentication](#authentication)
4. [API Overview](#api-overview)
5. [Document Ingestion](#document-ingestion)
   - [Ingesting Files](#ingesting-files)
   - [Ingesting Text](#ingesting-text)
6. [Querying the System](#querying-the-system)
   - [Basic Queries](#basic-queries)
   - [Advanced Queries](#advanced-queries)
7. [Using Agents](#using-agents)
   - [RAG Agent](#rag-agent)
   - [Conversation Agent](#conversation-agent)
   - [Multi-Tool Agent](#multi-tool-agent)
8. [Working with Chains](#working-with-chains)
   - [RAG Chain](#rag-chain)
   - [Summarization Chain](#summarization-chain)
   - [Question-Answering Chain](#question-answering-chain)
9. [Managing the Vector Index](#managing-the-vector-index)
   - [Viewing Index Statistics](#viewing-index-statistics)
   - [Updating Documents](#updating-documents)
   - [Deleting Documents](#deleting-documents)
10. [Conversation Management](#conversation-management)
11. [Observability and Monitoring](#observability-and-monitoring)
12. [Troubleshooting](#troubleshooting)
13. [Best Practices](#best-practices)
14. [API Reference](#api-reference)

## 1. Introduction

Welcome to the RAG-Enabled LLM Microservice User Guide. This system combines the power of Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG) techniques to provide sophisticated question-answering capabilities. This guide will walk you through all aspects of using the system, from setup to advanced features.

## 2. Getting Started

### System Requirements

- Python 3.8+
- Docker (for containerized deployment)
- 8GB RAM (minimum), 16GB RAM (recommended)
- 4 CPU cores (minimum), 8 CPU cores (recommended)

### Installation

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

### Configuration

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
   ```

3. Choose the appropriate YAML configuration file (`dev.yaml`, `prod.yaml`, or `test.yaml`) based on your environment.

## 3. Authentication

The API uses JWT (JSON Web Tokens) for authentication. To authenticate:

1. Obtain a token by sending a POST request to `/api/v1/auth/token` with your credentials.
2. Include the token in the `Authorization` header of subsequent requests:
   ```
   Authorization: Bearer <your_token>
   ```

## 4. API Overview

The API is organized into the following main endpoints:

- `/api/v1/ingest`: For document ingestion
- `/api/v1/query`: For querying the RAG system
- `/api/v1/agent`: For interacting with intelligent agents
- `/api/v1/chain`: For using processing chains
- `/api/v1/index`: For managing the vector index
- `/api/v1/conversation`: For managing conversations

Detailed API documentation is available at `/docs` when running the server.

## 5. Document Ingestion

### Ingesting Files

To ingest a file:

```http
POST /api/v1/ingest/file
Content-Type: multipart/form-data

file=@path/to/your/document.pdf
```

Supported file types: PDF, TXT, CSV, DOCX

### Ingesting Text

To ingest raw text:

```http
POST /api/v1/ingest/text
Content-Type: application/json

{
  "text": "Your text content here",
  "metadata": {
    "source": "manual input",
    "date": "2023-07-15"
  }
}
```

## 6. Querying the System

### Basic Queries

To perform a basic query:

```http
POST /api/v1/query
Content-Type: application/json

{
  "query": "What is machine learning?"
}
```

### Advanced Queries

For advanced queries with specific parameters:

```http
POST /api/v1/query/advanced
Content-Type: application/json

{
  "query": "Explain the concept of neural networks in detail",
  "max_tokens": 300,
  "temperature": 0.7
}
```

## 7. Using Agents

### RAG Agent

To use the RAG Agent:

```http
POST /api/v1/agent/run
Content-Type: application/json

{
  "agent_type": "rag",
  "params": {
    "query": "What are the main types of machine learning?"
  }
}
```

### Conversation Agent

To use the Conversation Agent:

```http
POST /api/v1/agent/run
Content-Type: application/json

{
  "agent_type": "conversation",
  "params": {
    "conversation_id": "user123",
    "message": "Tell me about artificial intelligence."
  }
}
```

### Multi-Tool Agent

To use the Multi-Tool Agent:

```http
POST /api/v1/agent/run
Content-Type: application/json

{
  "agent_type": "multi_tool",
  "params": {
    "query": "Summarize the key points about machine learning and then ask a follow-up question."
  }
}
```

## 8. Working with Chains

### RAG Chain

To use the RAG Chain:

```http
POST /api/v1/chain/run
Content-Type: application/json

{
  "chain_type": "rag",
  "inputs": {
    "query": "What is the capital of France?"
  }
}
```

### Summarization Chain

To use the Summarization Chain:

```http
POST /api/v1/chain/run
Content-Type: application/json

{
  "chain_type": "summarization",
  "inputs": {
    "text": "Long text to be summarized..."
  }
}
```

### Question-Answering Chain

To use the Question-Answering Chain:

```http
POST /api/v1/chain/run
Content-Type: application/json

{
  "chain_type": "qa",
  "inputs": {
    "question": "Who invented the telephone?",
    "context": "Alexander Graham Bell was an inventor who is credited with inventing the first practical telephone."
  }
}
```

## 9. Managing the Vector Index

### Viewing Index Statistics

To view index statistics:

```http
GET /api/v1/index/stats
```

### Updating Documents

To update a document in the index:

```http
PUT /api/v1/index/document
Content-Type: application/json

{
  "doc_id": "unique_document_id",
  "new_text": "Updated content of the document",
  "new_metadata": {
    "source": "manual update",
    "date": "2023-07-15"
  }
}
```

### Deleting Documents

To delete a document from the index:

```http
DELETE /api/v1/index/document/{doc_id}
```

## 10. Conversation Management

To manage a conversation:

```http
POST /api/v1/conversation/message
Content-Type: application/json

{
  "conversation_id": "user123",
  "message": "Tell me more about supervised learning."
}
```

To retrieve a conversation summary:

```http
GET /api/v1/conversation/{conversation_id}/summary
```

## 11. Observability and Monitoring

- Metrics are available at `/metrics` in Prometheus format.
- Logs are output in JSON format and can be collected by your logging infrastructure.
- Traces are sent to the configured OpenTelemetry collector.

## 12. Troubleshooting

Common issues and their solutions:

1. **Authentication Errors**: Ensure your API key is correct and not expired.
2. **Rate Limiting**: If you encounter rate limit errors, reduce the frequency of your requests.
3. **Ingestion Failures**: Check that your documents are in a supported format and not corrupted.
4. **Query Timeouts**: For complex queries, try breaking them down into simpler parts.

## 13. Best Practices

1. Use specific queries for better results.
2. Regularly update your document index to ensure fresh information.
3. Monitor your usage to optimize performance and costs.
4. Use conversation management for multi-turn interactions.
5. Implement proper error handling in your client applications.

## 14. API Reference

For a complete API reference, please refer to the OpenAPI documentation available at `/docs` when running the server.

This user guide provides a comprehensive overview of how to use the RAG-Enabled LLM Microservice. For further assistance or to report issues, please contact our support team or open an issue on the GitHub repository.