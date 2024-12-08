from kubernetes import client, config
from typing import List, Dict, Optional
from v1.models.registerservices.models import ServiceOnboarding
from base.k8s_config import load_k8s_config

# Load Kubernetes Configurations
v1_services, v1_ingresses = load_k8s_config()
custom_api = client.CustomObjectsApi()


def register_to_crd(service: client.V1Service) -> None:
    """
    Register a discovered service into the ServiceOnboarding CRD.
    """
    annotations = service.metadata.annotations if service.metadata.annotations else {}
    onboarding_status = (
        "discovered" if annotations.get("portal-discovery") == "true" else "ignored"
    )

    # Create a ServiceOnboarding instance
    onboarding = ServiceOnboarding(
        service_name=service.metadata.name,
        namespace=service.metadata.namespace,
        customer_id=annotations.get("customer-id", "unknown"),
        onboarding_status=onboarding_status,
        metadata=annotations,
    )

    try:
        # Register the ServiceOnboarding instance in Kubernetes
        custom_api.create_namespaced_custom_object(
            group="portal.itlusions.com",
            version="v1",
            namespace=service.metadata.namespace,
            plural="serviceonboardings",
            body=onboarding.to_dict(),
        )
        print(f"Service {service.metadata.name} registered in CRD.")
    except client.exceptions.ApiException as e:
        if e.status == 409:  # Resource already exists
            print(f"Service {service.metadata.name} already registered.")
        else:
            print(f"Error registering service {service.metadata.name}: {e}")
