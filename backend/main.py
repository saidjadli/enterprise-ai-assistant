from fastapi import FastAPI

from backend.api.routes import router


app = FastAPI(
    title="Enterprise Knowledge Assistant",
    version="0.1.0"
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "message": "Enterprise AI Assistant API"
    }