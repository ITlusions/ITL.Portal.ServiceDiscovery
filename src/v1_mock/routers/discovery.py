from fastapi import APIRouter
from v1_mock.controllers.servicediscovery.discovery import get_ingresses
from v1_mock.models.models import DiscoveredServices

router = APIRouter()

@router.get("/discovered-services", response_model=DiscoveredServices)
async def get_discovered_services():
    ingresses = get_ingresses()
    return DiscoveredServices(ingresses=ingresses)
