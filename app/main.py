# from fastapi import FastAPI
# from app.api import wildfires, deforestation

# app = FastAPI(
#     title="EcoGuard – AI Forest Monitoring",
#     version="1.0.0",
#     description="Wildfire & deforestation monitoring using satellite intelligence"
# )

# app.include_router(wildfires.router, prefix="/api")
# app.include_router(deforestation.router, prefix="/api")

# @app.get("/")
# def root():
#     return {
#         "status": "EcoGuard backend running",
#         "modules": ["wildfires", "deforestation"]
#     }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import wildfires, deforestation

app = FastAPI(
    title="EcoGuard – AI Forest Monitoring",
    version="1.0.0",
    description="Wildfire & deforestation monitoring using satellite intelligence"
)

# ✅ CORS CONFIG (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (DEV only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wildfires.router, prefix="/api")
app.include_router(deforestation.router, prefix="/api")

@app.get("/")
def root():
    return {
        "status": "EcoGuard backend running",
        "modules": ["wildfires", "deforestation"]
    }
