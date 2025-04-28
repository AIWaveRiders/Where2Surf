import pysurfline

def get_forecast_dataframe(spot_id):
    # Fetch the surf forecast
    forecasts = pysurfline.get_spot_forecasts(spot_id)
    # Convert to DataFrame
    df = forecasts.get_dataframe()
    return df

if __name__ == "__main__":
    spot_id = "5842041f4e65fad6a7708cfd"  # Replace with your preferred spot

    # Print the arguments that get_spot_forecasts can accept
    print("\n🛠️ get_spot_forecasts Arguments:")
    help(pysurfline.get_spot_forecasts)

    df = get_forecast_dataframe(spot_id)

    print("\n📊 Forecast DataFrame Columns:")
    print(df.columns.tolist())  # Show all available fields

    print("\n🔍 Sample Forecast Data:")
    print(df.head())

    print("\n📂 pysurfline Module Directory:")
    print(dir(pysurfline))  # List all attributes and methods in pysurfline
