import datetime
import os
import socket
from dotenv import load_dotenv
import requests
import json
from geopy.geocoders import Nominatim
import dateutil.parser
from dialogflowSession import dialogflowSession

load_dotenv()
# Dialogflow env variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

DIALOGFLOW_PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')
DIALOGFLOW_LANGUAGE_CODE = os.getenv('DIALOGFLOW_LANGUAGE_CODE')
SESSION_ID = os.getenv('SESSION_ID')
INTENT_NAME = os.getenv('INTENT_NAME')

# OpenWeatherMap env variable
OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')

# Server env variables
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))



def get_location(response):
    geolocator = Nominatim(user_agent="weather-bot")
    items = response.query_result.parameters.items()
    city = next(item for item in items if item[0] == "geo-city")[1]
    location = geolocator.geocode(city)
    return location


def get_date(response):
    items = response.query_result.parameters.items()
    date = next(item for item in items if item[0] == "date-time")[1]
    if not date:
        date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+02:00")
    elif not isinstance(date, str):
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


def process_weather_request(intent):
    location = get_location(intent)
    date = get_date(intent)
    report = get_weather(location, date)
    hourly_report = get_weather_by_hour(date, report)
    date = dateutil.parser.parse(date)
    return "🐵 " + date.strftime("%A %d %B %H %M") + ", we will have " + hourly_report["weather"][0]["description"] + \
        ", with " + str(hourly_report["temp"]) + " degrees\n"


def process_query(query, dialogflow_session):
    intent = dialogflow_session.get_intent(query)
    if intent.query_result.intent.display_name == INTENT_NAME and \
            intent.query_result.intent_detection_confidence >= 0.7:
        response = process_weather_request(intent)
    else:
        response = "🐒 Bro what do you mean ?\n"
    return response


def run_tcp_server(dialogflow_session):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    sock.bind(server_address)
    sock.listen(1)
    while True:
        print("Waiting for socket connection...")
        try:
            conn, addr = sock.accept()
        except KeyboardInterrupt:
            break
        try:
            print("New connection")
            while True:
                print(" waiting for question...")
                data = conn.recv(1024)
                if not data:
                    break
                response = process_query(query=data.decode(), dialogflow_session=dialogflow_session)
                conn.sendall(response.encode())
        except KeyboardInterrupt:
            conn.close()
            break
        finally:
            print("close")
            conn.close()


def main():
    dialogflow_session = dialogflowSession(DIALOGFLOW_PROJECT_ID, DIALOGFLOW_LANGUAGE_CODE, SESSION_ID)
    run_tcp_server(dialogflow_session)


if __name__ == "__main__":
    main()
