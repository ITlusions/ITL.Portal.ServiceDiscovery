from kubernetes import client, config
from typing import List, Dict
from models import Service, Ingress, ServiceEndpoint

# Load kubeconfig (assumes kubeconfig is correctly set)
config.load_kube_config()

# Initialize Kubernetes API clients
v1_services = client.CoreV1Api()
v1_ingresses = client.NetworkingV1Api()

# Function to get services and their API endpoints
def get_services() -> List[Service]:
    services_info = []
    
    # List all services across all namespaces
    services = v1_services.list_service_for_all_namespaces()
    
    for service in services.items:
        # Check if the service has the 'portal-discovery' annotation set to 'true'
        annotations = service.metadata.annotations if service.metadata.annotations else {}
        if annotations.get('portal-discovery') == 'true':
            # Get exposed ports
            endpoints = []
            for port in service.spec.ports:
                # Assume HTTP(S) services are exposed through port protocols
                protocol = port.protocol if port.protocol else 'TCP'
                # Optionally handle path, like "/api/v1"
                endpoints.append(ServiceEndpoint(protocol=protocol, port=port.port))
            
            # Collect service details including annotations if relevant
            service_info = Service(
                namespace=service.metadata.namespace,
                name=service.metadata.name,
                type=service.spec.type,
                annotations=annotations,
                endpoints=endpoints
            )
            services_info.append(service_info)
    
    return services_info

# Function to get ingresses and map routes
def get_ingresses() -> List[Ingress]:
    ingresses_data = []
    
    # Get ingresses from all namespaces
    ingresses = v1_ingresses.list_ingress_for_all_namespaces()

    for ingress in ingresses.items:
        # Collect details about each ingress, including paths
        ingress_info = Ingress(
            namespace=ingress.metadata.namespace,
            name=ingress.metadata.name,
            hosts=[rule.host for rule in ingress.spec.rules] if ingress.spec.rules else [],
            paths=[path.http.paths[0].path for path in ingress.spec.rules if path.http] if ingress.spec.rules else [],
            annotations=ingress.metadata.annotations if ingress.metadata.annotations else {}
        )
        ingresses_data.append(ingress_info)
    
    return ingresses_data
