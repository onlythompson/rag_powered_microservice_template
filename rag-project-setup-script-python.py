import os
import sys

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def create_file(path):
    directory = os.path.dirname(path)
    open(path, 'a').close()

def setup_project():
    # Project root
    root = os.getcwd()
    # Source directory structure
    src_dirs = [
        "src/core",
        "src/data/document_loaders",
        "src/data/data_connectors",
        "src/embeddings",
        "src/vectorstores",
        "src/llms",
        "src/chains",
        "src/prompts",
        "src/memory",
        "src/agents",
        "src/services",
        "src/api/routes",
        "src/api/schemas",
    ]

    for dir_path in src_dirs:
        create_directory(dir_path)

    # Test directory structure
    test_dirs = [
        "tests/unit/data",
        "tests/unit/embeddings",
        "tests/unit/vectorstores",
        "tests/unit/llms",
        "tests/unit/chains",
        "tests/unit/services",
        "tests/integration",
        "tests/e2e",
    ]

    for dir_path in test_dirs:
        create_directory(dir_path)

    # Other necessary directories
    other_dirs = [
        "scripts",
        "docs/api",
        "docs/architecture",
        "docs/user_guide",
        "config",
    ]

    for dir_path in other_dirs:
        create_directory(dir_path)

    # Create initial files
    files_to_create = [
        "src/core/__init__.py",
        "src/core/config.py",
        "src/core/constants.py",
        "src/core/logger.py",
        "src/data/__init__.py",
        "src/data/document_loaders/__init__.py",
        "src/data/data_connectors/__init__.py",
        "src/embeddings/__init__.py",
        "src/embeddings/embedding_models.py",
        "src/vectorstores/__init__.py",
        "src/vectorstores/custom_vectorstore.py",
        "src/llms/__init__.py",
        "src/llms/model_customizations.py",
        "src/chains/__init__.py",
        "src/chains/rag_chain.py",
        "src/chains/query_chain.py",
        "src/prompts/__init__.py",
        "src/prompts/custom_prompts.py",
        "src/memory/__init__.py",
        "src/memory/custom_memory.py",
        "src/agents/__init__.py",
        "src/agents/custom_agent.py",
        "src/services/__init__.py",
        "src/services/ingestion_service.py",
        "src/services/query_service.py",
        "src/services/index_service.py",
        "src/api/__init__.py",
        "src/api/main.py",
        "src/api/routes/__init__.py",
        "src/api/routes/ingest.py",
        "src/api/routes/query.py",
        "src/api/routes/manage.py",
        "src/api/schemas/__init__.py",
        "src/api/schemas/request_schemas.py",
        "src/api/schemas/response_schemas.py",
        "config/dev.yaml",
        "config/prod.yaml",
        "config/test.yaml",
        ".gitignore",
        "README.md",
        "requirements.txt",
        "setup.py",
        "docker-compose.yml",
        ".env",
    ]

    for file_path in files_to_create:
        create_file(file_path)

    print("Project structure created successfully!")

if __name__ == "__main__":
    setup_project()
