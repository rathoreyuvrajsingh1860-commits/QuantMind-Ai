from fastapi import FastAPI

from src.api.router import router


app = FastAPI(
    title="QuantMind AI",
    description="AI-powered financial intelligence platform.",
    version="0.1.0",
)

app.include_router(router)