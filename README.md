# Kubernetes Service Discovery with FastAPI

This project is a simple Kubernetes service discovery API built with **FastAPI**. It interacts with Kubernetes to retrieve services and ingresses from your cluster and exposes them through REST endpoints. This API is useful for service discovery in Kubernetes environments, especially for microservices architectures.

## Features

- **Service Discovery**: Fetches services from the Kubernetes cluster that have a specific annotation (`portal-discovery: true`).
- **Ingress Discovery**: Retrieves ingresses configured in the cluster, including associated hosts and paths.
- **FastAPI Integration**: Exposes services and ingresses data via REST endpoints.
- **Kubernetes Integration**: Automatically loads Kubernetes configuration either from the local `kubeconfig` or from the cluster if deployed inside a Kubernetes environment.

## Project Structure

```
D:.
│   docker-compose.yml
│   Dockerfile
│   README.md
│   requirements.txt
│
└───src
    │   main.py
    │
    ├───base
    │   └───config
    │       └── k8s_config.py
    │
    ├───controllers
    │   └───servicediscovery
    │       └── discovery.py
    │
    ├───models
    │   └── models.py
    │
    └───routers
        └── discovery.py
```

- **`main.py`**: Entry point of the FastAPI application.
- **`k8s_config.py`**: Loads the Kubernetes configuration.
- **`discovery.py` (Controller)**: Contains logic for fetching services and ingresses from the Kubernetes cluster.
- **`discovery.py` (Router)**: Exposes REST API endpoints for service discovery.
- **`models.py`**: Defines the data models used by the API.

## Setup

### Prerequisites

Before you begin, make sure you have the following installed:

- **Docker**
- **Docker Compose** (for running multi-container applications or just local-testing like I do)
- **Kubernetes Cluster** (or a local development setup with tools like [Minikube](https://minikube.sigs.k8s.io/docs/))
- **Python 3.11+** (if you want to run it locally without Docker)

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/ITlusions/ITL.Portal.ServiceDiscovery.git
    cd ITL.Portal.ServiceDiscovery
    ```

2. **Create and activate a virtual environment** (Optional but recommended for local development):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Kubernetes Configuration**:
   - If you are running the app **locally**, make sure you have your `KUBECONFIG` file (the Kubernetes configuration file) available.
   - If you are deploying **inside a Kubernetes cluster**, it will automatically use the cluster's internal configuration.

5. **Run the FastAPI app locally**:

    You can run the app using `uvicorn`:

    ```bash
    uvicorn src.main:app --reload
    ```

    This will start the FastAPI application on [http://127.0.0.1:8000](http://127.0.0.1:8000).

6. **Docker Setup**:

    If you'd like to run the app in a Docker container, use the `docker-compose.yml` file.

    - Build and start the containers:

      ```bash
      docker-compose up --build
      ```

    - This will run the FastAPI application inside a Docker container, exposing it on port `8000`.

## API Endpoints

### `GET /discovered-services`

Fetches the list of discovered services and ingresses from the Kubernetes cluster.

**Response**: Returns a JSON object with two fields:

- `services`: A list of services with details like name, namespace, type, and endpoints.
- `ingresses`: A list of ingresses with associated hosts and paths.

**Example**:

```json
{
  "ingresses": [
    {
      "namespace": "namespace-placeholder",
      "name": "ingress-placeholder",
      "hosts": [
        "example.com"
      ],
      "paths": [
        "/"
      ],
      "annotations": {
        "cert-manager.io/cluster-issuer": "issuer-placeholder",
        "external-dns.alpha.kubernetes.io/hostname": "example.com",
        "ingressClassName": "ingress-class-placeholder",
        "traefik.ingress.kubernetes.io/router.entrypoints": "web, websecure"
      }
    }
  ],
  "services": [
    {
      "namespace": "namespace-placeholder",
      "name": "service-placeholder",
      "type": "LoadBalancer",
      "annotations": {
        "external-dns.alpha.kubernetes.io/hostname": "service.example.com",
        "metallb.universe.tf/ip-allocated-from-pool": "vlan-placeholder",
        "portal-discovery": "true"
      },
      "endpoints": [
        {
          "protocol": "TCP",
          "port": 80,
          "path": null
        },
        {
          "protocol": "TCP",
          "port": 443,
          "path": null
        }
      ]
    }
  ]
}
```

## Environment Variables

The app uses the `KUBECONFIG` environment variable to determine the location of the Kubernetes config file. You can set it like this:

```bash
export KUBECONFIG=/path/to/your/kubeconfig
```

In a Kubernetes environment, the config will be automatically picked up from the cluster.

## Docker Compose

To run the application using Docker Compose, you can modify the `docker-compose.yml` to suit your environment. The `KUBECONFIG` file is mounted as a volume from your local machine to the container in the `docker-compose.yml`.

### Example `docker-compose.yml`

```yaml
version: "3.8"

services:
  fastapi:
    build: .
    ports:
      - "8000:8000"
    environment:
      - KUBECONFIG=/var/.kube/46004d8e-baf7-4306-82a3-3805b2e8e777
    volumes:
      - /path/to/kubeconfigs:/var/.kube
    command: ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
## Acknowledgments

- **FastAPI**: For building the API with minimal boilerplate.
- **Kubernetes Python Client**: For interacting with Kubernetes clusters in Python.
- **Uvicorn**: The ASGI server for FastAPI.

[Niels Weistra] @ [ITlusions]

   [ITlusions]: <https://www.itlusions.com>
   [Niels Weistra]: <mailto:n.weistra@itlusions.com>