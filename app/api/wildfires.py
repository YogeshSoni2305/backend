from fastapi import APIRouter
from app.services.firms import fetch_wildfires_india, fires_to_geojson

router = APIRouter()

@router.get("/wildfires")
def wildfires():
    fires = fetch_wildfires_india()

    return {
        "country": "India",
        "count": len(fires),
        "alert": "🔥 Active wildfires detected" if fires else "✅ No wildfires",
        "geojson": fires_to_geojson(fires)
    }
