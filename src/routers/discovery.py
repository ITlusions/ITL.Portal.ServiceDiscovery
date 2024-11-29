from fastapi import APIRouter
from controllers.servicediscovery.discovery import get_services, get_ingresses
from models.models import DiscoveredServices

router = APIRouter()

@router.get("/discovered-services", response_model=DiscoveredServices)
async def get_discovered_services():
    ingresses = get_ingresses()
    services = get_services()
    return DiscoveredServices(ingresses=ingresses, services=services)
