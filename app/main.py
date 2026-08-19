from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="SkillBridge")
app.include_router(router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
