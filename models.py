import requests

class WeatherReport:
    """Encapsulates current weather data."""
    def __init__(self, city: str, country: str, temp: float, feels_like: float,
                 humidity: int, pressure: int, condition: str, wind_speed: float):
        self.city = city
        self.country = country
        self.temp = temp
        self.feels_like = feels_like
        self.humidity = humidity
        self.pressure = pressure
        self.condition = condition
        self.wind_speed = wind_speed

class WeatherFetcher:
    """Manages API calls to OpenWeatherMap."""
    CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
    FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_current_weather(self, city: str) -> WeatherReport:
        params = {"q": city, "appid": self.api_key, "units": "metric"}
        try:
            response = requests.get(self.CURRENT_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return WeatherReport(
                city=data["name"],
                country=data["sys"]["country"],
                temp=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                humidity=data["main"]["humidity"],
                pressure=data["main"]["pressure"],
                condition=data["weather"][0]["description"].title(),
                wind_speed=data["wind"]["speed"]
            )
        except requests.exceptions.HTTPError:
            raise ValueError(f"City '{city}' not found.")
        except requests.exceptions.RequestException as exc:
            raise ConnectionError(f"Network error: {exc}")

    def get_forecast(self, city: str) -> tuple[list[str], list[float]]:
        """Returns timestamps and temperatures for the 24-hour forecast trend."""
        params = {"q": city, "appid": self.api_key, "units": "metric"}
        try:
            response = requests.get(self.FORECAST_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # 8 intervals of 3 hours = 24 hours
            timestamps = [item["dt_txt"][11:16] for item in data["list"][:8]]
            temps = [item["main"]["temp"] for item in data["list"][:8]]
            return timestamps, temps
        except requests.exceptions.HTTPError:
            raise ValueError(f"Unable to fetch forecast for '{city}'.")
        except requests.exceptions.RequestException as exc:
            raise ConnectionError(f"Network error: {exc}")