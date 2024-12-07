from kubernetes import client, config
from typing import List, Dict, Optional
from v1.models.models import Service, Ingress, ServiceEndpoint
from v1.controllers.registerservices.controller import register_to_crd
from base.k8s_config import load_k8s_config

v1_services, v1_ingresses = load_k8s_config()


def get_services(
    annotation_key: Optional[str] = None,
    annotation_value: Optional[str] = None,
    register: bool = False,
) -> List[Service]:
    """
    Fetches services, optionally filtered by annotation key and value.

    Parameters:
    - annotation_key: The key of the annotation to filter services by (optional).
    - annotation_value: The value of the annotation to filter services by (optional).
    - register: Whether to register the discovered services in the ServiceOnboarding CRD (default: True).

    Returns:
    - List of services that match the optional annotation filter.
    """
    services_info = []
    services = v1_services.list_service_for_all_namespaces()

    for service in services.items:
        annotations = (
            service.metadata.annotations if service.metadata.annotations else {}
        )
        # Check if the service matches the provided annotation filter
        if annotation_key and annotation_value:
            if annotations.get(annotation_key) == annotation_value:
                endpoints = []
                for port in service.spec.ports:
                    protocol = port.protocol if port.protocol else "TCP"
                    endpoints.append(ServiceEndpoint(protocol=protocol, port=port.port))

                service_info = Service(
                    namespace=service.metadata.namespace,
                    name=service.metadata.name,
                    type=service.spec.type,
                    annotations=annotations,
                    endpoints=endpoints,
                )
                services_info.append(service_info)
                if register:
                    register_to_crd(service)
        else:
            # If no filter is provided, return all services with the 'portal-discovery' annotation
            if annotations.get("portal-discovery") == "true":
                endpoints = []
                for port in service.spec.ports:
                    protocol = port.protocol if port.protocol else "TCP"
                    endpoints.append(ServiceEndpoint(protocol=protocol, port=port.port))

                service_info = Service(
                    namespace=service.metadata.namespace,
                    name=service.metadata.name,
                    type=service.spec.type,
                    annotations=annotations,
                    endpoints=endpoints,
                )
                services_info.append(service_info)
                if register:
                    register_to_crd(service)

    return services_info


def get_ingresses() -> List[Ingress]:
    ingresses_data = []
    ingresses = v1_ingresses.list_ingress_for_all_namespaces()
    for ingress in ingresses.items:
        ingress_info = Ingress(
            namespace=ingress.metadata.namespace,
            name=ingress.metadata.name,
            hosts=(
                [rule.host for rule in ingress.spec.rules] if ingress.spec.rules else []
            ),
            paths=(
                [path.http.paths[0].path for path in ingress.spec.rules if path.http]
                if ingress.spec.rules
                else []
            ),
            annotations=(
                ingress.metadata.annotations if ingress.metadata.annotations else {}
            ),
        )
        ingresses_data.append(ingress_info)
    return ingresses_data
