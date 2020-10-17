# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting the weather of a city. """

import json
from datetime import datetime

import requests
from pytz import country_names as c_n
from pytz import country_timezones as c_tz
from pytz import timezone as tz

from userbot import CMD_HELP
from userbot import OPEN_WEATHER_MAP_APPID as OWM_API
from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.modules.dbhelper import get_weather, set_weather

# ===== CONSTANT =====
INV_PARAM = "`Invalid parameters. Try again!`"
NO_API_KEY = "`Get an API key from` https://openweathermap.org/ `first.`"
DB_FAILED = "`Database connections failed!`"


# ====================
async def get_tz(con):
    """
    Get time zone of the given country.
    Credits: @aragon12 and @zakaryan2004.
    """
    for c_code in c_n:
        if con == c_n[c_code]:
            return tz(c_tz[c_code][0])
    try:
        if c_n[con]:
            return tz(c_tz[con][0])
    except KeyError:
        return


@register(outgoing=True, pattern="^.weather(?: |$)(.*)")
async def fetch_weather(weather):
    """ For .weather command, gets the current weather of a city. """
    if OWM_API is None:
        await weather.edit(NO_API_KEY)
        return

    OpenWeatherAPI = OWM_API
    saved_props = await get_weather() if is_mongo_alive() else None

    if not weather.pattern_match.group(1):
        if 'weather_city' in saved_props:
            city = saved_props['weather_city']
        else:
            await weather.edit("`Please specify a city or set one as default.`"
                               )
            return
    else:
        city = weather.pattern_match.group(1)

    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items() for timezone in timezones
    }

    if "," in city:
        newcity = city.split(",")
        if len(newcity[1]) == 2:
            city = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f'{country}']
            except KeyError:
                await weather.edit(INV_PARAM)
                return
            city = newcity[0].strip() + "," + countrycode.strip()

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OpenWeatherAPI}'
    request = requests.get(url)
    result = json.loads(request.text)

    if request.status_code != 200:
        await weather.edit(INV_PARAM)
        return

    cityname = result['name']
    curtemp = result['main']['temp']
    humidity = result['main']['humidity']
    min_temp = result['main']['temp_min']
    max_temp = result['main']['temp_max']
    desc = result['weather'][0]
    desc = desc['main']
    country = result['sys']['country']
    sunrise = result['sys']['sunrise']
    sunset = result['sys']['sunset']
    wind = result['wind']['speed']
    winddir = result['wind']['deg']

    ctimezone = tz(c_tz[country][0])
    time = datetime.now(ctimezone).strftime("%A, %I:%M %p")
    fullc_n = c_n[f"{country}"]
    # dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    #        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    div = (360 / len(dirs))
    funmath = int((winddir + (div / 2)) / div)
    findir = dirs[funmath % len(dirs)]
    kmph = str(wind * 3.6).split(".")
    mph = str(wind * 2.237).split(".")

    def fahrenheit(fahr):
        temp = str(((fahr - 273.15) * 9 / 5 + 32)).split(".")
        return temp[0]

    def celsius(celc):
        temp = str((celc - 273.15)).split(".")
        return temp[0]

    def sun(unix):
        suntime = datetime.fromtimestamp(unix,
                                         tz=ctimezone).strftime("%I:%M %p")
        return suntime

    await weather.edit(
        f"**Temperature:** `{celsius(curtemp)}°C | {fahrenheit(curtemp)}°F`\n"
        +
        f"**Min. Temp.:** `{celsius(min_temp)}°C | {fahrenheit(min_temp)}°F`\n"
        +
        f"**Max. Temp.:** `{celsius(max_temp)}°C | {fahrenheit(max_temp)}°F`\n"
        + f"**Humidity:** `{humidity}%`\n" +
        f"**Wind:** `{kmph[0]} kmh | {mph[0]} mph, {findir}`\n" +
        f"**Sunrise:** `{sun(sunrise)}`\n" +
        f"**Sunset:** `{sun(sunset)}`\n\n\n" + f"**{desc}**\n" +
        f"`{cityname}, {fullc_n}`\n" + f"`{time}`")

@register(outgoing=True, pattern="^.forecast(?: |$)(.*)")
async def fetch_forecast(weather):
    """ For .weather command, gets the current weather of a city. """
    if OWM_API is None:
        await weather.edit(NO_API_KEY)
        return

    OpenWeatherAPI = OWM_API
    saved_props = await get_weather() if is_mongo_alive() else None
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat=50.04&lon=21.99&APPID={OpenWeatherAPI}'
    request = requests.get(url)
    if request.status_code != 200:
        await weather.edit(INV_PARAM)
        return
    result = json.loads(request.text)
    hourly = result['hourly']
    weather_string = f"**Forecast**:\n"
    for forecast in hourly[:12]:
      time = str(datetime.fromtimestamp(forecast["dt"]))[11:]
      temp = f"{round(forecast['temp'] - 273.15, 2)}°C"
      descriptions = [description['description'] for description in forecast['weather']]
      description_string = ', '.join(descriptions)
      forecast_line = f"**{time}** - `{temp}`, `{description_string}`\n"
      weather_string += forecast_line
    weather_string += "\n\n\n" + f"**{desc}**\n" + f"`{cityname}, {fullc_n}`\n" + f"`{time}`"
    weather.edit(weather_string)
    
@register(outgoing=True, pattern="^.setcity(?: |$)(.*)")
async def set_default_city(scity):
    """ For .setcity command, change the default
        city for weather command. """
    if not is_mongo_alive() or not is_redis_alive():
        await scity.edit(DB_FAILED)
        return

    if OWM_API is None:
        await scity.edit(NO_API_KEY)
        return

    OpenWeatherAPI = OWM_API

    if not scity.pattern_match.group(1):
        await scity.edit("`Please specify a city to set one as default.`")
        return
    else:
        city = scity.pattern_match.group(1)

    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items() for timezone in timezones
    }

    if "," in city:
        newcity = scity.split(",")
        if len(newcity[1]) == 2:
            city = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f'{country}']
            except KeyError:
                await scity.edit(INV_PARAM)
                return
            city = newcity[0].strip() + "," + countrycode.strip()

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OpenWeatherAPI}'
    request = requests.get(url)
    result = json.loads(request.text)

    if request.status_code != 200:
        await scity.edit(INV_PARAM)
        return

    await set_weather(city)
    cityname = result['name']
    country = result['sys']['country']

    fullc_n = c_n[f"{country}"]

    await scity.edit(f"`Set default city as {cityname}, {fullc_n}.`")


CMD_HELP.update({"weather": ["Weather",
    " - `.weather <city> or .weather <city>, <country name/code>`: "
    "Gets the weather of a city.\n"
    " - `.setcity <city> or .setcity <city>, <country name/code>`: "
    "Set the default city for the .weather command.\n"]
})
