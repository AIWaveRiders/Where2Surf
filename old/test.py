import requests
import json

# Replace this with a real spot ID — you can get these from Surfline's site (they're in the URL)
spot_id = "5842041f4e65fad6a7708805"  # Example: Steamer Lane, Santa Cruz

# This is one of Surfline’s forecast endpoints
url = "https://services.surfline.com/kbyg/spots/forecasts"

# Request parameters
params = {
    "spotId": spot_id,
    "days": 6,  # Max number of days (can be adjusted)
    "intervalHours": 1,  # Forecast interval
    "maxHeights": True,  # Whether to include max heights
    "unit": "us"  # 'us' for feet, 'uk' for meters
}

response = requests.get(url, params=params)

# Raise an error if the request failed
response.raise_for_status()

# Pretty print the full JSON response
forecast_data = response.json()
print(json.dumps(forecast_data, indent=2))
