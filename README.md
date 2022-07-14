# Bono the bonobo weather-bot

LOCAL (for now) weather bot using Dialogflow API to detect intent and OpenWeatherMap API to get the weather.


## Prerequisites

- Python (install [from here](https://www.python.org/downloads/))
- Dialogflow Agent trained with weather questions
- OpenWeatherMap API key (get your own [from here](https://openweathermap.org/api))

## Setup

1. Clone this repository
  ```bash
  $ git clone https://github.com/AdrienCastelbou/weather-bot
  ```

2. Move to this repository
  ```bash
  $ cd weather-bot
  ```

3. Create a new virtual environment
  ```bash
  $ python3 -m venv venv
  $ ./venv/bin/activate
  ```

4. Install the requirements
  ```bash
  $ pip install -r requirements.txt
  ```

5. Add your Google private_key.json into the project
```bash
.
├── README.md
├── main.py
├── private_key.json
├── requirements.txt
└── venv
```

6. Create your .env file
```bash
$ touch .env
```

7. Add your Dialogflow project id into the .env file
```bash
DIALOGFLOW_PROJECT_ID='my-dialogflow-project-id'
```

8. Complete your .env file with these two environnement variables
```bash
DIALOGFLOW_LANGUAGE_CODE='en'
SESSION_ID='me'
```

9. Add your [OpenWeatherMap API key](https://home.openweathermap.org/api_keys) into the .env file
```bash
OPEN_WEATHER_API_KEY='MyAPIKey'
 ```
 
 10. That it ! Now you can run the script with your question in argument !
 ```bash
 $ python3 main.py "What will be the weather in Paris in two hours ?"
 $ Thursday 14 July 17 22 we will have few clouds , with  31.11  degrees
 
