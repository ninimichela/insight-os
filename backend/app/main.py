from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.content import router as content_router

app = FastAPI(title="INSight OS API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(content_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "insight-os-api"}
