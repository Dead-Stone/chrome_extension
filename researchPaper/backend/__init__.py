from fastapi import FastAPI
from backend.routes import router as api_router

def create_app():
    app = FastAPI()

    # Register routers
    app.include_router(api_router)

    return app
