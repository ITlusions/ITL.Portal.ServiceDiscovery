import sys
import logging
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from httpx import AsyncClient
from main import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_health():
    logger.info("Starting test for /health endpoint...")

    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/health")
        
        # Log response details for debugging
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response Body: {response.json()}")

    # Enhanced assertions with clear error messages
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}. Response: {response.json()}"
    #assert "services" in response.json(), f"Missing 'services' key in response: {response.json()}"
    #assert "ingresses" in response.json(), f"Missing 'ingresses' key in response: {response.json()}"

    logger.info("Test for /health endpoint passed successfully.")
