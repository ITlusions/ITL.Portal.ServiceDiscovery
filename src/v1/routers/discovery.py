from fastapi import APIRouter, HTTPException
from typing import Optional
from v1.controllers.servicediscovery.discovery import (
    get_services as controller_get_services,
    get_ingresses as controller_get_ingresses,
)
from v1.models.models import DiscoveredServices, ServiceFilterRequest

router = APIRouter()


async def fetch_services_and_ingresses(
    annotation_key: Optional[str] = None, annotation_value: Optional[str] = None
):
    """Helper function to fetch services and ingresses."""
    try:
        services = controller_get_services(
            annotation_key=annotation_key, annotation_value=annotation_value
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching services: {str(e)}"
        )

    try:
        ingresses = controller_get_ingresses()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f"Error fetching ingresses: {str(e)}"
        )

    return DiscoveredServices(services=services, ingresses=ingresses)


@router.get(
    "/discovered-services",
    response_model=DiscoveredServices,
    summary="Discover services and ingresses",
    description="Retrieve all services and ingresses based on optional annotation filters.",
    tags=["Service Discovery"],
)
async def get_discovered_services(
    annotation_key: Optional[str] = None, annotation_value: Optional[str] = None
):
    """Retrieve services and ingresses based on optional annotation filters."""
    return await fetch_services_and_ingresses(annotation_key, annotation_value)


@router.post(
    "/discovered-services",
    response_model=DiscoveredServices,
    summary="Filter and discover services and ingresses",
    description="Filter services and ingresses using a request body with annotation filters.",
    tags=["Service Discovery"],
)
async def post_discovered_services(filter_request: ServiceFilterRequest):
    """Filter services and ingresses based on annotation filters provided in the request body."""
    return await fetch_services_and_ingresses(
        annotation_key=filter_request.annotation_key,
        annotation_value=filter_request.annotation_value,
    )


@router.get(
    "/get-services",
    response_model=DiscoveredServices,
    summary="Get services",
    description="Retrieve services based on optional annotation filters.",
    tags=["Service Discovery"],
)
async def get_services_route(
    annotation_key: Optional[str] = None, annotation_value: Optional[str] = None
):
    """Retrieve services based on optional annotation filters."""
    try:
        services = controller_get_services(
            annotation_key=annotation_key, annotation_value=annotation_value
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f"Error fetching services: {str(e)}"
        )
    return DiscoveredServices(services=services)


@router.get(
    "/get-ingresses",
    response_model=DiscoveredServices,
    summary="Get ingresses",
    description="Retrieve all ingresses.",
    tags=["Service Discovery"],
)
async def get_ingresses_route():
    """Retrieve all ingresses."""
    try:
        ingresses = controller_get_ingresses()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f"Error fetching ingresses: {str(e)}"
        )
    return DiscoveredServices(ingresses=ingresses)
