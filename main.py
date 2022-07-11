import os
import sys
import dialogflow
from dotenv import load_dotenv
from google.api_core.exceptions import InvalidArgument
import requests
import json
from geopy.geocoders import Nominatim
import dateutil.parser

load_dotenv()
# Dialogflow env variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

DIALOGFLOW_PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')
DIALOGFLOW_LANGUAGE_CODE = os.getenv('DIALOGFLOW_LANGUAGE_CODE')
SESSION_ID = os.getenv('SESSION_ID')

# OpenWeatherMap env variable
OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')


def get_intent(query):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text= query, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        if response.query_result.intent.display_name != "get-weather" or \
                response.query_result.intent_detection_confidence < 0.7:
            print("Do you want the weather ?")
            exit()
    except InvalidArgument:
        print("bouhou")
        raise
    return response


def get_location(response):
    geolocator = Nominatim(user_agent="weather-bot")
    items = response.query_result.parameters.items()

    date = next(item for item in items if item[0] == "date-time")[1]
    city = next(item for item in items if item[0] == "geo-city")[1]
    if not isinstance(date, str):
        date_item = date.items()
        date = date_item[0][1]
    location = geolocator.geocode(city)
    return location


def get_date(response):
    items = response.query_result.parameters.items()
    date = next(item for item in items if item[0] == "date-time")[1]
    if not isinstance(date, str):
        date_item = date.items()
        date = date_item[0][1]
    return date


def get_weather_by_hour(wanted_date, report):
    wanted_date = dateutil.parser.parse(wanted_date)
    dt = wanted_date.timestamp()
    hourly_report = report["hourly"]
    for entry in hourly_report:
        if entry["dt"] >= dt:
            return entry


def get_weather(location, date):
    open_weather_url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % \
                       (location.latitude, location.longitude, OPEN_WEATHER_API_KEY)
    response = requests.get(open_weather_url)
    report = json.loads(response.text)
    return report


def main():
    if len(sys.argv) != 2:
        print('Bad number of arguments')
        return 1
    query = sys.argv[1]
    response = get_intent(query)
    location = get_location(response)
    date = get_date(response)
    report = get_weather(location, date)
    hourly_report = get_weather_by_hour(date, report)
    date = dateutil.parser.parse(date)
    print(date.strftime("%A %d %B %H %M"), "we will have", hourly_report["weather"][0]["description"], ", with ",
          hourly_report["temp"],
          " degrees")
    return 0


if __name__ == "__main__":
    main()
