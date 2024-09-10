# RAG-Enabled LLM Microservice API Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Base URL](#base-url)
3. [Authentication](#authentication)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [Endpoints](#endpoints)
   - [Authentication](#authentication-1)
   - [Document Ingestion](#document-ingestion)
   - [Querying](#querying)
   - [Agents](#agents)
   - [Chains](#chains)
   - [Index Management](#index-management)
   - [Conversation Management](#conversation-management)
   - [Observability](#observability)

## 1. Introduction

This document provides a detailed description of the RAG-Enabled LLM Microservice API. The API allows you to ingest documents, perform queries, use various agents and chains, manage the vector index, and handle conversations.

## 2. Base URL

All API requests should be made to:

```
https://api.yourdomain.com/api/v1
```

Replace `yourdomain.com` with your actual domain.

## 3. Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## 4. Error Handling

The API uses standard HTTP response codes. In case of an error, the response body will contain more information about the error.

Example error response:

```json
{
  "error": {
    "code": "BAD_REQUEST",
    "message": "Invalid input: Query cannot be empty"
  }
}
```

## 5. Rate Limiting

The API is rate-limited to prevent abuse. The current limits are:

- 100 requests per minute for authenticated users
- 10 requests per minute for unauthenticated users

If you exceed the rate limit, you'll receive a 429 Too Many Requests response.

## 6. Endpoints

### Authentication

#### Login

Authenticate and receive a JWT token.

- **URL**: `/auth/token`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer"
    }
    ```

### Document Ingestion

#### Ingest File

Upload and ingest a document file.

- **URL**: `/ingest/file`
- **Method**: `POST`
- **Headers**: 
  - `Content-Type: multipart/form-data`
- **Request Body**:
  - `file`: The file to be ingested
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "message": "File ingested successfully",
      "document_id": "doc_123456"
    }
    ```

#### Ingest Text

Ingest raw text data.

- **URL**: `/ingest/text`
- **Method**: `POST`
- **Headers**: 
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "text": "Your text content here",
    "metadata": {
      "source": "manual input",
      "date": "2023-07-15"
    }
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "message": "Text ingested successfully",
      "document_id": "doc_123457"
    }
    ```

### Querying

#### Basic Query

Perform a basic query on the ingested documents.

- **URL**: `/query`
- **Method**: `POST`
- **Headers**: 
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "query": "What is machine learning?"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "query": "What is machine learning?",
      "answer": "Machine learning is a branch of artificial intelligence...",
      "source_documents": [
        {
          "content": "Machine learning is a method of data analysis that automates analytical model building...",
          "metadata": {
            "source": "ML_textbook.pdf",
            "page": 15
          }
        }
      ]
    }
    ```

#### Advanced Query

Perform an advanced query with additional parameters.

- **URL**: `/query/advanced`
- **Method**: `POST`
- **Headers**: 
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "query": "Explain the concept of neural networks in detail",
    "max_tokens": 300,
    "temperature": 0.7
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "query": "Explain the concept of neural networks in detail",
      "answer": "Neural networks are a series of algorithms that aim to recognize underlying relationships in a set of data...",
      "source_documents": [
        {
          "content": "Neural networks, also known as artificial neural networks (ANNs) or simulated neural networks (SNNs), are a subset of machine learning...",
          "metadata": {
            "source": "deep_learning_guide.pdf",
            "page": 42
          }
        }
      ]
    }
    ```

### Agents

#### Run Agent

Execute a specific type of agent.

- **URL**: `/agent/run`
- **Method**: `POST`
- **Headers**: 
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "agent_type": "rag",
    "params": {
      "query": "What are the main types of machine learning?"
    }
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "result": "The main types of machine learning are:\n1. Supervised Learning\n2. Unsupervised Learning\n3. Reinforcement Learning\n...",
      "agent_type": "rag",
      "execution_time": 2.5
    }
    ```

### Chains

#### Run Chain

Execute a specific type of processing chain.

- **URL**: `/chain/run`
- **Method**: `POST`
- **Headers**: 
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "chain_type": "summarization",
    "inputs": {
      "text": "Long text to be summarized..."
    }
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "result": {
        "summary": "This is a concise summary of the input text..."
      },
      "chain_type": "summarization",
      "execution_time": 1.8
    }
    ```

### Index Management

#### Get Index Stats

Retrieve statistics about the vector index.

- **URL**: `/index/stats`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "total_documents": 10000,
      "total_vectors": 15000,
      "index_size": "1.2 GB"
    }
    ```

#### Update Document

Update an existing document in the index.

- **URL**: `/index/document`
- **Method**: `PUT`
- **Headers**: 
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "doc_id": "doc_123456",
    "new_text": "Updated content of the document",
    "new_metadata": {
      "source": "manual update",
      "date": "2023-07-15"
    }
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "message": "Document updated successfully",
      "doc_id": "doc_123456"
    }
    ```

#### Delete Document

Remove a document from the index.

- **URL**: `/index/document/{doc_id}`
- **Method**: `DELETE`
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "message": "Document deleted successfully",
      "doc_id": "doc_123456"
    }
    ```

### Conversation Management

#### Send Message

Send a message in a conversation context.

- **URL**: `/conversation/message`
- **Method**: `POST`
- **Headers**: 
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "conversation_id": "conv_789012",
    "message": "Tell me more about supervised learning."
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "response": "Supervised learning is a type of machine learning where the algorithm learns from labeled data...",
      "conversation_id": "conv_789012"
    }
    ```

#### Get Conversation Summary

Retrieve a summary of a conversation.

- **URL**: `/conversation/{conversation_id}/summary`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "conversation_id": "conv_789012",
      "summary": "This conversation covered topics related to machine learning, focusing on supervised learning techniques..."
    }
    ```

### Observability

#### Get Metrics

Retrieve system metrics in Prometheus format.

- **URL**: `/metrics`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200
  - **Content**: Prometheus-formatted metrics

This API documentation provides a comprehensive overview of the endpoints available in the RAG-Enabled LLM Microservice. For any additional information or support, please contact our development team.