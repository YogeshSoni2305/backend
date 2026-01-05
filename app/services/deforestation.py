def get_deforestation_summary():
    loss = 7.4

    risk = (
        "High" if loss > 10
        else "Medium" if loss > 5
        else "Low"
    )

    return {
        "region": "Central India (Sample)",
        "satellite": "Sentinel-2",
        "method": "NDVI Change Detection",
        "start_year": 2020,
        "end_year": 2024,
        "forest_loss_percent": loss,
        "risk_level": risk,
        "status": "⚠️ Deforestation Detected",
        "recommendation": "Increase monitoring and restrict logging activity",
        "note": "Computed using Google Earth Engine (cloud-based)"
    }
