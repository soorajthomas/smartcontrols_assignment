import requests


def get_hotel_list():
    url = 'https://api.myjson.com/bins/tl0bp'
    api_request = requests.get(url=url)
    if api_request.status_code == 200:
        hotels = api_request.json()
        if 'hotels' in hotels:
            return hotels['hotels']
    return []
