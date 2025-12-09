import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
SHEETY_KEY = os.environ.get("SHEETY_KEY")
APP_ENDPOINT = os.environ.get("BASE_URL")
TRACKER_ENDPOINT = os.environ.get("TRACKER_ENDPOINT")

url = f"{APP_ENDPOINT}/v1/nutrition/natural/exercise"

headers = {
    "Content-Type": "application/json",
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

user_query = input("Tell me about your exercise: ")

user_parameters = {
    "query": user_query,
    "gender": "female",
    "age": 30,
    "weight_kg": 55,
    "height_cm": 160
}
sheety_headers = {
    "Authorization": f"Bearer {SHEETY_KEY}"
}

response = requests.post(url, headers=headers, json=user_parameters)
response.raise_for_status()
result = response.json()

exercise_data = result["exercises"][0]

now = datetime.now()
entry_date = now.strftime("%m-%d-%Y")
entry_time = now.strftime("%H:%M %p")

exercise = exercise_data["name"].title()
duration = exercise_data["duration_min"]
calories = exercise_data["nf_calories"]

entry_params = {
    "workout": {
        "date": entry_date,
        "time": entry_time,
        "exercise": exercise,
        "duration": duration,
        "calories": calories
    }
}


sheety_response = requests.post(TRACKER_ENDPOINT, headers=sheety_headers, json=entry_params)
print(sheety_response.status_code)
print(sheety_response.text)
sheety_response.raise_for_status()
