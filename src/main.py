from fastapi import FastAPI

app = FastAPI(
    title="QuantMind AI",
    description="AI-powered financial intelligence platform.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "quantmind-ai",
    }