from fastapi import FastAPI
from discovery import get_services, get_ingresses
from models import DiscoveredServices

app = FastAPI()

@app.get("/discovered-services", response_model=DiscoveredServices)
async def get_discovered_services():
    # Retrieve discovered services and ingresses
    ingresses = get_ingresses()
    services = get_services()

    # Return data encapsulated in DiscoveredServices model
    return DiscoveredServices(ingresses=ingresses, services=services)
