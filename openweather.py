from utils.setup import load_config
from utils.settings import get_addon_settings

import requests
from datetime import datetime


USER_SETTINGS = get_addon_settings("openweather")
UNITS = {"standard": "kelvin", "metric": "celcius", "imperial": "fahrenheit"}


def call_api():
    base_url = f"https://api.openweathermap.org/data/2.5/onecall"

    params = {
        "lat": USER_SETTINGS["lat"],
        "lon": USER_SETTINGS["long"],
        "units": USER_SETTINGS["units"],
        "appid": USER_SETTINGS["api_key"],
    }

    return requests.get(base_url, params=params).json()


def say_weather(voice_instance):
    response = call_api()
    now = response["current"]

    voice_output = ""

    for weather in now["weather"]:
        voice_output += (
            f"{weather['description']} "
            "with a temperature of "
            f"{now['temp'] : .0f} degrees {UNITS[USER_SETTINGS['units']]} "
        )

    # check for any alerts
    try:
        for alert in response["alert"]:
            voice_output += (
                f"alert from {alert['sender_name']} "
                f"{alert['event']} {alert['description']} "
            )
    except:
        pass

    # check for rain and snow
    if "rain" in now:
        voice_output += f"with {now['rain']['1h']} milimeters of rain "
    elif "snow" in now:
        voice_output += f"with {now['snow']['1h']} milimeters of snow "

    voice_instance.say(voice_output)


def say_seven_day_forecast(voice_instance):
    response = call_api()

    daily = response["daily"]

    voice_output = ""

    for day in daily:
        for weather in day["weather"]:
            voice_output += (
                "on "
                f"{datetime.fromtimestamp(day['dt']).strftime('%A')} "
                "it will be "
                f"{weather['description']} "
                "with a maximum temperature of "
                f"{day['temp']['max'] : .0f} degress"
                f"{UNITS[USER_SETTINGS['units']]} "
                f"and minimum temperature of "
                f"{day['temp']['min'] : .0f} degrees"
                f"{UNITS[USER_SETTINGS['units']]}, "
            )

    voice_instance.say(voice_output)


def execute_query(query, voice_instance):
    actions = {
        "weather": say_weather,
        "forecast": say_seven_day_forecast,
    }

    actions[query](voice_instance)


def parse_query(command):
    query = None

    if "weather" in command:
        query = "weather"
    elif "forecast" in command:
        query = "forecast"

    return query


def run(command, args, voice_instance):

    query = parse_query(command)
    execute_query(query, voice_instance)
