# MultiVecStream - Multi-Vector Database File Processor

A real-time file monitoring system that automatically processes files and stores their vector embeddings in various vector databases.

## Features

- **Real-time file monitoring** - Watches a folder for new/modified files
- **Multi-format support** - Processes PDF, DOCX, CSV, Excel, images, and text files
- **Multiple vector databases** - Supports Qdrant, Pinecone, Weaviate, Milvus, and Redis
- **Automatic vector generation** - Uses SentenceTransformers for text and pixel-based vectors for images

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Vector Database

Edit `config.py` to set your vector database credentials:

```python
# For Qdrant
QDRANT_URL = "http://localhost:6333"
QDRANT_API_KEY = "your-api-key"

# For Pinecone
PINECONE_API_KEY = "your-pinecone-api-key"
PINECONE_ENVIRONMENT = "us-west1-gcp"

# For Weaviate
WEAVIATE_URL = "http://localhost:8080"

# For Milvus
MILVUS_URI = "localhost:19530"
MILVUS_USER = "root"
MILVUS_PASSWORD = "Milvus"

# For Redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379
```

### 3. Run the Application

```bash
python Main.py
```

The application will:
1. Prompt you to select a vector database (1-5)
2. Create a `watch-folder` directory if it doesn't exist
3. Start monitoring the folder for file changes

## Supported File Types

- **Text files**: `.txt`, `.xml` - Uses SentenceTransformers for embeddings
- **Documents**: `.pdf`, `.docx` - Extracts text and creates embeddings
- **Spreadsheets**: `.csv`, `.xlsx` - Processes each row as text
- **Images**: `.png`, `.jpg`, `.jpeg` - Uses pixel-based vectors (224x224 resized)

## Vector Database Setup

### Qdrant
```bash
# Run Qdrant locally
docker run -p 6333:6333 qdrant/qdrant
```

### Pinecone
- Sign up at [pinecone.io](https://pinecone.io)
- Create an index with dimension 512 and metric "cosine"

### Weaviate
```bash
# Run Weaviate locally
docker run -p 8080:8080 semitechnologies/weaviate:1.22.4
```

### Milvus
```bash
# Run Milvus locally
docker-compose up -d
```

### Redis
```bash
# Run Redis locally
docker run -p 6379:6379 redis:alpine
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install missing dependencies with `pip install -r requirements.txt`
2. **Connection errors**: Ensure your vector database is running and accessible
3. **Permission errors**: Check file permissions for the watch folder

### Configuration

- Edit `config.py` to change database settings
- The system automatically creates collections/indexes if they don't exist
- Vector dimensions are standardized to 512 for compatibility

## File Structure

```
MultiVecStream/
├── Main.py              # Main application entry point
├── config.py            # Configuration settings
├── db_router.py         # Routes to appropriate vector database
├── qdrant_client.py     # Qdrant client implementation
├── pinecone_client.py   # Pinecone client implementation
├── weaviate_client.py   # Weaviate client implementation
├── milvus_client.py     # Milvus client implementation
├── redis_client.py      # Redis client implementation
├── watch-folder/        # Monitored folder (created automatically)
└── README.md           # This file
``` 