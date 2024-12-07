from typing import Optional, Dict


class ServiceOnboarding:
    """
    Represents the ServiceOnboarding CRD structure.
    """

    def __init__(
        self,
        service_name: str,
        namespace: str,
        customer_id: Optional[str] = "unknown",
        onboarding_status: Optional[str] = "discovered",
        metadata: Optional[Dict[str, str]] = None,
    ):
        self.api_version = "portal.itlusions.com/v1"
        self.kind = "ServiceOnboarding"
        self.metadata = {"name": f"{service_name}-onboarding"}
        self.spec = {
            "serviceName": service_name,
            "namespace": namespace,
            "customerId": customer_id,
            "onboardingStatus": onboarding_status,
            "metadata": metadata or {},
        }

    def to_dict(self) -> Dict:
        """
        Convert the ServiceOnboarding object to a dictionary.
        """
        return {
            "apiVersion": self.api_version,
            "kind": self.kind,
            "metadata": self.metadata,
            "spec": self.spec,
        }
