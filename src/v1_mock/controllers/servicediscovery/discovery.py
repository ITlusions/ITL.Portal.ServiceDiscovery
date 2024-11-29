from kubernetes import client, config
from typing import List, Dict
from v1_mock.models.models import Service, Ingress, ServiceEndpoint
from v1_mock.base.config.k8s_config import load_k8s_config

v1_services, v1_ingresses = load_k8s_config()

def get_services() -> List[Service]:
    services_info = []
    services = v1_services.list_service_for_all_namespaces()
    for service in services.items:
        # Check if the service has the 'portal-discovery' annotation set to 'true'
        annotations = service.metadata.annotations if service.metadata.annotations else {}
        if annotations.get('portal-discovery') == 'true':
            endpoints = []
            for port in service.spec.ports:
                protocol = port.protocol if port.protocol else 'TCP'
                # Optionally handle path, like "/api/v1"
                endpoints.append(ServiceEndpoint(protocol=protocol, port=port.port))
            service_info = Service(
                namespace=service.metadata.namespace,
                name=service.metadata.name,
                type=service.spec.type,
                annotations=annotations,
                endpoints=endpoints
            )
            services_info.append(service_info)
    return services_info

def get_ingresses() -> List[Ingress]:
    ingresses_data = []
    ingresses = v1_ingresses.list_ingress_for_all_namespaces()
    for ingress in ingresses.items:
        ingress_info = Ingress(
            namespace=ingress.metadata.namespace,
            name=ingress.metadata.name,
            hosts=[rule.host for rule in ingress.spec.rules] if ingress.spec.rules else [],
            paths=[path.http.paths[0].path for path in ingress.spec.rules if path.http] if ingress.spec.rules else [],
            annotations=ingress.metadata.annotations if ingress.metadata.annotations else {}
        )
        ingresses_data.append(ingress_info)
    return ingresses_data
