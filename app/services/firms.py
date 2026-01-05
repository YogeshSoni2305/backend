import requests, csv
from io import StringIO

NASA_FIRMS_API_KEY = "e0c752fa3a8bbf19a5055615deacbbc6"

def fetch_wildfires_india():
    url = (
        f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
        f"{NASA_FIRMS_API_KEY}/VIIRS_SNPP_NRT/world/1"
    )

    r = requests.get(url, timeout=15)
    text = r.text

    if "<html>" in text.lower():
        raise RuntimeError("Invalid FIRMS MAP_KEY")

    reader = csv.DictReader(StringIO(text))
    fires = []

    for row in reader:
        lat = float(row["latitude"])
        lon = float(row["longitude"])

        # 🇮🇳 India bounding box
        if 6 <= lat <= 37 and 68 <= lon <= 97:
            brightness = float(row["bright_ti4"])
            severity = (
                "high" if brightness > 330
                else "medium" if brightness > 310
                else "low"
            )

            fires.append({
                "latitude": lat,
                "longitude": lon,
                "brightness": brightness,
                "confidence": row["confidence"],
                "severity": severity,
                "date": row["acq_date"]
            })

    return fires


def fires_to_geojson(fires):
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [f["longitude"], f["latitude"]]
                },
                "properties": {
                    "severity": f["severity"],
                    "brightness": f["brightness"],
                    "date": f["date"]
                }
            }
            for f in fires
        ]
    }

