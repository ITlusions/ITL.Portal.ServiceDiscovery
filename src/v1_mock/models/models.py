from pydantic import BaseModel
from typing import List, Optional, Dict

class ServiceEndpoint(BaseModel):
    protocol: str
    port: int
    path: Optional[str] = None

class Service(BaseModel):
    namespace: str
    name: str
    type: str
    annotations: Optional[Dict[str, str]] = {}
    endpoints: List[ServiceEndpoint] = []

class Ingress(BaseModel):
    namespace: str
    name: str
    hosts: List[str]
    paths: List[str]
    annotations: Optional[Dict[str, str]] = {}

class DiscoveredServices(BaseModel):
    ingresses: List[Ingress]
    services: List[Service]