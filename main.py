from fastapi import FastAPI
from routes.example_routes import router

app = FastAPI()

app.include_router(router)