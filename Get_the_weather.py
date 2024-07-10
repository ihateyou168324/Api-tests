import requests
import time
BASE_URL = "https://api.weather.gov"

def get_grid_points(latitude, longitude):
    """Get the grid points for the given latitude and longitude."""
    endpoint = f"{BASE_URL}/points/{latitude},{longitude}"
    
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        grid_data = response.json()
        grid_id = grid_data['properties']['gridId']
        grid_x = grid_data['properties']['gridX']
        grid_y = grid_data['properties']['gridY']
        return grid_id, grid_x, grid_y
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None, None, None

def get_weather_forecast(latitude, longitude):
    """Get the weather forecast for the given latitude and longitude."""
    grid_id, grid_x, grid_y = get_grid_points(latitude, longitude)
    if grid_id and grid_x and grid_y:
        endpoint = f"{BASE_URL}/gridpoints/{grid_id}/{grid_x},{grid_y}/forecast"
        request = BASE_URL + endpoint
        print(request)
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            weather_data = response.json()
            forecast = weather_data['properties']['periods']
            for period in forecast:
                print(f"Forecast for {period['name']}: {period['detailedForecast']}")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
    else:
        print("Failed to get grid points. Unable to fetch weather forecast.")

# Example usage: Get weather forecast for Washington DC (latitude: 38.89511, longitude: -77.03637)
lat = input('What is your latitude?\n')
long = input('What is your longitude?\n')
get_weather_forecast(lat, long)
print("Autoclosing in 60 seconds")
time.sleep(60)
