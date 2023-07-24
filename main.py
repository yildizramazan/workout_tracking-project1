import os

import requests
from datetime import datetime


APP_ID = os.environ["ENV_NIX_APP_ID"]
API_KEY = os.environ["ENV_NIX_API_KEY"]

USER_NAME = os.environ["ENV_SHEETY_USERNAME"]
PASSWORD = os.environ["ENV_SHEETY_PASSWORD"]

GENDER = "male"
WEIGHT_KG = 81
HEIGHT_CM = 181
AGE = 19

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_text = input("Tell me which exercises you did: ")

sheet_endpoint = os.environ["ENV_SHEETY_ENDPOINT"]


headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}


#{'exercises': [{'tag_id': 317, 'user_input': 'ran', 'duration_min': 40.02, 'met': 9.8, 'nf_calories': 529.46, 'photo': {'highres': 'https://d2xdmhkmkbyw75.cloudfront.net/exercise/317_highres.jpg', 'thumb': 'https://d2xdmhkmkbyw75.cloudfront.net/exercise/317_thumb.jpg', 'is_user_uploaded': False}, 'compendium_code': 12050, 'name': 'running', 'description': None, 'benefits': None}]}
#{'exercises': [{'tag_id': 63, 'user_input': 'swim', 'duration_min': 30, 'met': 6, 'nf_calories': 243, 'photo': {'highres': 'https://d2xdmhkmkbyw75.cloudfront.net/exercise//63_highres.jpg', 'thumb': 'https://d2xdmhkmkbyw75.cloudfront.net/exercise//63_thumb.jpg', 'is_user_uploaded': False}, 'compendium_code': 18310, 'name': 'swimming', 'description': None, 'benefits': None}]}

exercise_response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = exercise_response.json()


date_now = datetime.now().strftime("%d""/""%m""/""%Y")
time_now = datetime.now().strftime("%X")


for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": date_now,
            "time": time_now,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    sheet_response = requests.post(
        url=sheet_endpoint,
        json=sheet_inputs,
        auth=(
            USER_NAME,
            PASSWORD,
        )
    )
    print(sheet_response.text)