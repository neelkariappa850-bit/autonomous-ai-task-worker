from fastapi import FastAPI

app = FastAPI(
    title="Autonomous AI Task Worker",
    description="AI worker that autonomously executes computer-based tasks",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Autonomous AI Worker is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }