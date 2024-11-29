from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from v1.routers.discovery import router as v1_discovery_router
from v1_mock.routers.discovery import router as v1_mock_discovery_router

app = FastAPI()
app_v1 = FastAPI(servers=[
        {"url": "/v1", "description": "V1 environment"},
        {"url": "https://api.itlusions.com/servicediscovery/v1", "description": "V1 environment"}
    ]
)
app_v1_mock = FastAPI(servers=[
        {"url": "/v1_mock", "description": "V1_mock environment"},
        {"url": "https://api.itlusions.com/servicediscovery/v1_mock", "description": "V1_mock environment"}
    ]
)

app_v1.include_router(v1_discovery_router)
app_v1_mock.include_router(v1_mock_discovery_router)

app.mount("/v1", app_v1)
app.mount("/v1_mock", app_v1_mock)

@app.get("/")
async def root():
    return RedirectResponse(url="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
