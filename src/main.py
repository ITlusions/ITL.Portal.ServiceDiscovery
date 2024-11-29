from fastapi import FastAPI
from routers.discovery import router as discovery_router

app = FastAPI()
app.include_router(discovery_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
