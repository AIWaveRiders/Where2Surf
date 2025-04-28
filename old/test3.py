import requests
import json

spot_id = "5842041f4e65fad6a7708805"
url = "https://services.surfline.com/kbyg/spots/forecasts"

params = {
    "spotId": spot_id,
    "days": 16,
    "intervalHours": 1,
    "maxHeights": True,
    "unit": "us"
}

# Paste your token here
headers = {
    "Authorization": "Bearer YOUR_TOKEN_HERE"
}

response = requests.get(url, params=params, headers=headers)
response.raise_for_status()

forecast_data = response.json()
print(json.dumps(forecast_data, indent=2))
