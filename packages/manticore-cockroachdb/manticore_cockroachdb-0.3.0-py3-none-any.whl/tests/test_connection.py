"""Test database connection directly."""

import os
import sys
import asyncio
import logging
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manticore_cockroachdb.async_database import AsyncDatabase
from manticore_cockroachdb.database import Database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_sync_connection():
    """Test synchronous database connection."""
    logger.info("Testing synchronous database connection...")
    
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        db = Database.from_url(database_url)
        logger.info(f"Connected to {db.host}:{db.port}/{db.database}")
    else:
        db = Database(database="test_db")
        logger.info("Connected to local database")
    
    try:
        result = db.execute("SELECT version()")
        logger.info(f"Database version: {result[0]['version']}")
        logger.info("Synchronous connection test successful!")
    except Exception as e:
        logger.error(f"Synchronous connection failed: {e}")
    finally:
        db.close()

async def test_async_connection():
    """Test asynchronous database connection."""
    logger.info("Testing asynchronous database connection...")
    
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        db = AsyncDatabase.from_url(database_url)
        logger.info(f"Created async connection to {db.host}:{db.port}/{db.database}")
    else:
        db = AsyncDatabase(database="test_db")
        logger.info("Created async connection to local database")
    
    try:
        await db.connect()
        result = await db.execute("SELECT version()")
        logger.info(f"Database version: {result[0]['version']}")
        logger.info("Asynchronous connection test successful!")
    except Exception as e:
        logger.error(f"Asynchronous connection failed: {e}")
    finally:
        await db.close()

if __name__ == "__main__":
    # Test sync connection
    test_sync_connection()
    
    # Test async connection
    asyncio.run(test_async_connection()) 