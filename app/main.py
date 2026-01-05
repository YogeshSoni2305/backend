from fastapi import FastAPI
from app.api import wildfires, deforestation

app = FastAPI(
    title="EcoGuard – AI Forest Monitoring",
    version="1.0.0",
    description="Wildfire & deforestation monitoring using satellite intelligence"
)

app.include_router(wildfires.router, prefix="/api")
app.include_router(deforestation.router, prefix="/api")

@app.get("/")
def root():
    return {
        "status": "EcoGuard backend running",
        "modules": ["wildfires", "deforestation"]
    }
