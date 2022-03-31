import requests
import config

def parse_weather(lat_and_lon):
    api_key = config.api_weather_key

    if type(lat_and_lon) != list:
        return '/weather argument (place) not found'

    lat = lat_and_lon[0]
    lon = lat_and_lon[1]
    exclude = "daily"

    resp_en = requests.get('https://api.openweathermap.org/data/2.5/onecall?',
                        params={'lat': str(lat), 'lon': str(lon),
                                'exclude': str(exclude), 'appid': api_key,
                                'units': 'metric'})

    resp_ru = requests.get('https://api.openweathermap.org/data/2.5/onecall?',
                        params={'lat': str(lat), 'lon': str(lon),
                                'exclude': str(exclude), 'appid': api_key,
                                'units': 'metric', 'lang': 'ru'})

    response_json_en = resp_en.json()
    timezone_en = response_json_en["timezone"]
    hourly_temp_en = response_json_en["hourly"][0]["temp"]
    hourly_temp_feels_en = response_json_en["hourly"][0]["feels_like"]
    hourly_pressure_en = response_json_en["hourly"][0]["pressure"]
    sky_en = response_json_en["hourly"][0]["weather"][0]["description"]

    response_json_ru = resp_ru.json()
    sky_ru = response_json_ru["hourly"][0]["weather"][0]["description"]

    weather_dict = {"timezone": f'{timezone_en}', "temp": f'{hourly_temp_en}',
                    "temp_feels": f'{hourly_temp_feels_en}', "pressure": f'{hourly_pressure_en}',
                    "sky_ru": f'{sky_ru}', "sky_en": f'{sky_en}'}

    return weather_dict


if __name__ == '__main__':
    pass
