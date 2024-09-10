#!/bin/bash

# RAG Project Setup Script

# Create main project directory
mkdir -p rag_microservice
cd rag_microservice

# Create source directory structure
mkdir -p src/{core,data/{document_loaders,data_connectors},embeddings,vectorstores,llms,chains,prompts,memory,agents,services,api/{routes,schemas}}

# Create test directory structure
mkdir -p tests/{unit/{data,embeddings,vectorstores,llms,chains,services},integration,e2e}

# Create other necessary directories
mkdir -p scripts docs/{api,architecture,user_guide} config

# Create initial files
touch src/core/{__init__.py,config.py,constants.py,logger.py}
touch src/data/{__init__.py,document_loaders/__init__.py,data_connectors/__init__.py}
touch src/embeddings/{__init__.py,embedding_models.py}
touch src/vectorstores/{__init__.py,custom_vectorstore.py}
touch src/llms/{__init__.py,model_customizations.py}
touch src/chains/{__init__.py,rag_chain.py,query_chain.py}
touch src/prompts/{__init__.py,custom_prompts.py}
touch src/memory/{__init__.py,custom_memory.py}
touch src/agents/{__init__.py,custom_agent.py}
touch src/services/{__init__.py,ingestion_service.py,query_service.py,index_service.py}
touch src/api/{__init__.py,main.py,routes/{__init__.py,ingest.py,query.py,manage.py},schemas/{__init__.py,request_schemas.py,response_schemas.py}}

# Create config files
touch config/{dev.yaml,prod.yaml,test.yaml}

# Create root level files
touch {.gitignore,README.md,requirements.txt,setup.py,docker-compose.yml,.env}

echo "Project structure created successfully!"
