import requests
import config

def get_places_coord(name):
    api_key = config.api_geocoder_key
    resp = requests.get('https://geocode-maps.yandex.ru/1.x/?',
                        params={'format': 'json', 'apikey': api_key, 'geocode': str(name)}).json()
    found = resp["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"]
    if found == '0':
        return False
    coord = (resp["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(' ')[::-1])
    return coord


if __name__ == '__main__':
    pass
