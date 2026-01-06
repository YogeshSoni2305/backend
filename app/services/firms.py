# import requests, csv
# from io import StringIO

# NASA_FIRMS_API_KEY = "e0c752fa3a8bbf19a5055615deacbbc6"

# # def fetch_wildfires_india():
# #     url = (
# #         f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
# #         f"{NASA_FIRMS_API_KEY}/VIIRS_SNPP_NRT/world/1"
# #     )

# #     r = requests.get(url, timeout=15)
# #     text = r.text

# #     if "<html>" in text.lower():
# #         raise RuntimeError("Invalid FIRMS MAP_KEY")

# #     reader = csv.DictReader(StringIO(text))
# #     fires = []

# #     for row in reader:
# #         lat = float(row["latitude"])
# #         lon = float(row["longitude"])

# #         # 🇮🇳 India bounding box
# #         if 6 <= lat <= 37 and 68 <= lon <= 97:
# #             brightness = float(row["bright_ti4"])
# #             severity = (
# #                 "high" if brightness > 330
# #                 else "medium" if brightness > 310
# #                 else "low"
# #             )

# #             fires.append({
# #                 "latitude": lat,
# #                 "longitude": lon,
# #                 "brightness": brightness,
# #                 "confidence": row["confidence"],
# #                 "severity": severity,
# #                 "date": row["acq_date"]
# #             })

# #     return fires

# def fetch_wildfires_india():
#     def fetch_from_firms(source: str, days: int):
#         url = (
#             f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
#             f"{NASA_FIRMS_API_KEY}/{source}/world/{days}"
#         )

#         r = requests.get(url, timeout=15)
#         text = r.text

#         if "<html>" in text.lower():
#             raise RuntimeError("Invalid NASA FIRMS API key")

#         reader = csv.DictReader(StringIO(text))
#         fires = []

#         for row in reader:
#             try:
#                 lat = float(row["latitude"])
#                 lon = float(row["longitude"])
#             except (ValueError, KeyError):
#                 continue

#             # 🇮🇳 India bounding box
#             if not (6 <= lat <= 37 and 68 <= lon <= 97):
#                 continue

#             try:
#                 brightness = float(row.get("bright_ti4", 0))
#             except ValueError:
#                 continue

#             # 🔥 Improved severity thresholds (VIIRS realistic)
#             if brightness >= 325:
#                 severity = "high"
#             elif brightness >= 300:
#                 severity = "medium"
#             else:
#                 severity = "low"

#             fires.append({
#                 "latitude": lat,
#                 "longitude": lon,
#                 "brightness": brightness,
#                 "confidence": row.get("confidence"),
#                 "severity": severity,
#                 "date": row.get("acq_date"),
#                 "source": source,
#             })

#         return fires

#     # 1️⃣ Try Near Real-Time first (today)
#     fires = fetch_from_firms("VIIRS_SNPP_NRT", 1)

#     # 2️⃣ Fallback to last 7 days if empty
#     if not fires:
#         fires = fetch_from_firms("VIIRS_SNPP", 7)

#     return fires


# def fires_to_geojson(fires):
#     return {
#         "type": "FeatureCollection",
#         "features": [
#             {
#                 "type": "Feature",
#                 "geometry": {
#                     "type": "Point",
#                     "coordinates": [f["longitude"], f["latitude"]]
#                 },
#                 "properties": {
#                     "severity": f["severity"],
#                     "brightness": f["brightness"],
#                     "date": f["date"]
#                 }
#             }
#             for f in fires
#         ]
#     }




import requests
import csv
from io import StringIO

# ⚠️ In production, move this to env variable
NASA_FIRMS_API_KEY = "e0c752fa3a8bbf19a5055615deacbbc6"

# 🇮🇳 India bounding box
INDIA_LAT_RANGE = (6, 37)
INDIA_LON_RANGE = (68, 97)


def fetch_wildfires_india():
    """
    Fetch wildfire detections for India using NASA FIRMS.
    Strategy:
    1. Try Near Real-Time (last 24 hours)
    2. Fallback to last 7 days if empty
    """

    def fetch_from_firms(source: str, days: int):
        url = (
            f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
            f"{NASA_FIRMS_API_KEY}/{source}/world/{days}"
        )

        response = requests.get(url, timeout=15)
        text = response.text

        # API key / quota error
        if "<html>" in text.lower():
            raise RuntimeError("Invalid or expired NASA FIRMS API key")

        reader = csv.DictReader(StringIO(text))
        fires = []

        for row in reader:
            try:
                lat = float(row["latitude"])
                lon = float(row["longitude"])
                brightness = float(row.get("bright_ti4", 0))
            except (ValueError, KeyError):
                continue

            # 🇮🇳 India filter
            if not (
                INDIA_LAT_RANGE[0] <= lat <= INDIA_LAT_RANGE[1]
                and INDIA_LON_RANGE[0] <= lon <= INDIA_LON_RANGE[1]
            ):
                continue

            # 🔥 Severity classification (VIIRS-realistic)
            if brightness >= 325:
                severity = "high"
            elif brightness >= 300:
                severity = "medium"
            else:
                severity = "low"

            fires.append({
                "latitude": lat,
                "longitude": lon,
                "brightness": brightness,
                "confidence": row.get("confidence"),
                "severity": severity,
                "date": row.get("acq_date"),
                "source": source,
            })

        return fires

    # 1️⃣ Near real-time (today)
    fires = fetch_from_firms("VIIRS_SNPP_NRT", 1)

    # 2️⃣ Fallback (last 7 days)
    if not fires:
        fires = fetch_from_firms("VIIRS_SNPP", 7)

    return fires


def fires_to_geojson(fires):
    """
    Convert wildfire list to GeoJSON FeatureCollection
    """
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [f["longitude"], f["latitude"]],
                },
                "properties": {
                    "severity": f["severity"],
                    "brightness": f["brightness"],
                    "date": f["date"],
                },
            }
            for f in fires
        ],
    }


# 🔎 Optional local test
if __name__ == "__main__":
    fires = fetch_wildfires_india()
    print("Total fires detected:", len(fires))
