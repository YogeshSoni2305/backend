from fastapi import APIRouter
from app.services.deforestation import get_deforestation_summary

router = APIRouter()

@router.get("/deforestation")
def deforestation():
    return get_deforestation_summary()
