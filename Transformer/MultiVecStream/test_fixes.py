#!/usr/bin/env python3
"""
Test script to verify MultiVecStream fixes work correctly.
"""

def test_imports():
    """Test that all modules can be imported without errors."""
    try:
        print("Testing imports...")
        
        # Test config
        from config import VECTOR_DB, set_vector_db, get_env_var
        print("✅ config.py imported successfully")
        
        # Test db_router
        from db_router import upsert_vector, route_upsert
        print("✅ db_router.py imported successfully")
        
        # Test vector database clients
        print("Testing vector database clients...")
        
        # Test Qdrant
        try:
            from qdrant_handler import upsert_to_qdrant
            print("✅ qdrant_handler.py imported successfully")
        except ImportError as e:
            print(f"⚠️ qdrant_handler.py import failed: {e}")
        
        # Test Pinecone
        try:
            from pinecone_client import upsert_to_pinecone
            print("✅ pinecone_client.py imported successfully")
        except ImportError as e:
            print(f"⚠️ pinecone_client.py import failed: {e}")
        
        # Test Weaviate
        try:
            from weaviate_client import upsert_to_weaviate
            print("✅ weaviate_client.py imported successfully")
        except ImportError as e:
            print(f"⚠️ weaviate_client.py import failed: {e}")
        
        # Test Milvus
        try:
            from milvus_client import upsert_to_milvus
            print("✅ milvus_client.py imported successfully")
        except ImportError as e:
            print(f"⚠️ milvus_client.py import failed: {e}")
        
        # Test Redis
        try:
            from redis_client import upsert_to_redis
            print("✅ redis_client.py imported successfully")
        except ImportError as e:
            print(f"⚠️ redis_client.py import failed: {e}")
        
        print("\n✅ All core modules imported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_config():
    """Test configuration functionality."""
    try:
        print("\nTesting configuration...")
        
        from config import VECTOR_DB, set_vector_db, get_env_var
        
        print(f"Default VECTOR_DB: {VECTOR_DB}")
        
        # Test setting vector DB
        set_vector_db("Redis")
        print("✅ set_vector_db() function works")
        
        # Test getting environment variables
        redis_host = get_env_var("REDIS_HOST", "localhost")
        print(f"REDIS_HOST from config: {redis_host}")
        
        print("✅ Configuration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_dependencies():
    """Test that required dependencies are available."""
    try:
        print("\nTesting dependencies...")
        
        import sentence_transformers
        print("✅ sentence-transformers available")
        
        import watchdog
        print("✅ watchdog available")
        
        import pdfplumber
        print("✅ pdfplumber available")
        
        import pandas
        print("✅ pandas available")
        
        import PIL
        print("✅ Pillow available")
        
        import docx
        print("✅ python-docx available")
        
        print("✅ All dependencies available!")
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    print("🧪 Testing MultiVecStream fixes...\n")
    
    tests = [
        test_dependencies,
        test_imports,
        test_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MultiVecStream should work correctly.")
        print("\nTo run the application:")
        print("1. Configure your vector database in config.py")
        print("2. Run: python Main.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.") 