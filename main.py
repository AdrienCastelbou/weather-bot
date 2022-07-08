import os
import sys
import dialogflow
from dotenv import load_dotenv
from google.api_core.exceptions import InvalidArgument
import requests
import json
from geopy.geocoders import Nominatim

load_dotenv()
# Dialogflow env variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

DIALOGFLOW_PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')
DIALOGFLOW_LANGUAGE_CODE = os.getenv('DIALOGFLOW_LANGUAGE_CODE')
SESSION_ID = os.getenv('SESSION_ID')

# OpenWeatherMap env variables
OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')


session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
text_input = dialogflow.types.TextInput(text= sys.argv[1], language_code=DIALOGFLOW_LANGUAGE_CODE)
query_input = dialogflow.types.QueryInput(text=text_input)
try:
    response = session_client.detect_intent(session=session, query_input=query_input)
    if (response.query_result.intent.display_name != "get-weather" or response.query_result.intent_detection_confidence < 0.7):
        print("Do you want the weather ?")
        exit()
except InvalidArgument:
    print("bouhou")
    raise
geolocator = Nominatim(user_agent="weather-bot")
items = response.query_result.parameters.items()

date = next(item for item in items if item[0] == "date-time")[1]
city = next(item for item in items if item[0] == "geo-city")[1]
if (not isinstance(date, str)):
    date_item = date.items()
    date = date_item[0][1]
location = geolocator.geocode(city)
lat = location.latitude
lon = location.longitude
open_weather_url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, OPEN_WEATHER_API_KEY)
response = requests.get(open_weather_url)
data = json.loads(response.text)
print(date, " we will have ", data["current"]["weather"][0]["description"], ", with ", data["current"]["temp"], " degrees")