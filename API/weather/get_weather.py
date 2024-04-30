import os
from typing import Union

import requests
from dotenv.main import load_dotenv

from API.weather.get_location_user_computer import get_location


def weather_request(response_for_key) -> Union[str, list]:
    if response_for_key.status_code == 200:
        json_response = response_for_key.json()
        key_location = json_response[0]['Key']
        response = requests.get(f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{key_location}'
                                f'?apikey={os.getenv("ACCUWEATHER_KEY")}')
        if response.status_code == 200:
            json_response_2 = response.json()
            weather_info_days = []
            weather_info_one_day = ''
            for daily_weather in json_response_2['DailyForecasts']:
                key = daily_weather['Date']
                bad_index = key.index('T')
                data_day = key[:bad_index]
                temp_min_need = int(daily_weather['Temperature']['Minimum']['Value'])
                temp_max_need = int(daily_weather['Temperature']['Maximum']['Value'])
                description = daily_weather['Day']['IconPhrase']
                temp_min_need, temp_max_need = (temp_min_need - 32) * 5 / 9, (temp_max_need - 32) * 5 / 9
                data_weather = {
                    'Дата дня': '📅' + data_day,
                    'Минимальная температура': '❄' + str(int(temp_min_need)),
                    'Максимальная температура': '🔥' + str(int(temp_max_need)),
                    'Какая погода сегодня?': '🌏' + description
                }
                for key in data_weather:
                    weather_info_one_day += key + str(data_weather[key]) + ' '
                weather_info_days.append(weather_info_one_day)
                weather_info_one_day = ''
            return weather_info_days
        else:
            f'{response.status_code}-----{response.reason}'
    else:
        return f'{response_for_key.status_code}-----{response_for_key.reason}'


def get_weather_5_day(city_entered=None):
    load_dotenv()
    info_location = get_location()
    if not city_entered:
        response_for_key = requests.get(f'http://dataservice.accuweather.com/locations/v1/cities/search?'
                                        f'apikey={os.getenv("ACCUWEATHER_KEY")}'
                                        f'&q={info_location["city"]}&language=en')
        weather_request(response_for_key)
    else:
        response_for_key = requests.get(f'http://dataservice.accuweather.com/locations/v1/cities/search?'
                                        f'apikey={os.getenv("ACCUWEATHER_KEY")}'
                                        f'&q={city_entered}&language=en')
        weather_request(response_for_key)
