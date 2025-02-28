"""Test utilities for the Manticore CockroachDB client."""

import os
import pytest
import socket
import time
from functools import wraps

def is_cockroachdb_running(host="localhost", port=26257, timeout=1):
    """Check if CockroachDB is running and accessible.
    
    Args:
        host: Database host
        port: Database port
        timeout: Connection timeout in seconds
        
    Returns:
        True if CockroachDB is running, False otherwise
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def requires_database(f):
    """Skip test if database is not available."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Check if DATABASE_URL is set or if local CockroachDB is running
        if os.environ.get("DATABASE_URL") or is_cockroachdb_running():
            return f(*args, **kwargs)
        else:
            pytest.skip("No database available")
    return wrapper

def requires_async_database(f):
    """Skip async test if database is not available."""
    @wraps(f)
    async def wrapper(*args, **kwargs):
        # Check if DATABASE_URL is set or if local CockroachDB is running
        if os.environ.get("DATABASE_URL") or is_cockroachdb_running():
            return await f(*args, **kwargs)
        else:
            pytest.skip("No database available")
    return wrapper 