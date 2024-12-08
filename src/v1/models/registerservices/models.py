from pydantic import BaseModel, Field
from typing import Optional, Dict

class ServiceOnboardingSpec(BaseModel):
    serviceName: str
    namespace: str
    customerId: Optional[str] = "unknown"
    onboardingStatus: Optional[str] = "discovered"
    metadata: Optional[Dict[str, str]] = {}

class ServiceOnboarding(BaseModel):
    apiVersion: str = "portal.itlusions.com/v1"
    kind: str = "ServiceOnboarding"
    metadata: Dict[str, str] = Field(default_factory=lambda: {"name": ""})
    spec: ServiceOnboardingSpec

    class Config:
        # Ensure that the field names in the output match the expected names
        allow_population_by_field_name = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set metadata name dynamically
        self.metadata['name'] = f"{self.spec.serviceName}-onboarding"

    def to_dict(self) -> Dict:
        """Convert the ServiceOnboarding object to a dictionary."""
        return self.model_dump(by_alias=True)