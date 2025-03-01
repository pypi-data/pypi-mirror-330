"""Configure pytest for async tests."""

import pytest
import os

# Register the anyio plugin
pytest_plugins = ["anyio"]

# Configure anyio to use asyncio backend
@pytest.fixture
def anyio_backend():
    """Configure anyio to use asyncio backend."""
    return "asyncio" 