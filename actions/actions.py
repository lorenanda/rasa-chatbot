import requests
import json
import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
#from dotenv import load_dotenv
#load_dotenv()
import config.py

airtable_api_key = config.AIRTABLE_API_KEY
base_id = config.BASE_ID
table_name = config.TABLE_NAME

def create_health_log(confirm_exercise, exercise, sleep, diet, stress, goal):
    request_url = f"https://api.airtable.com/v0/{base_id}/{table_name}"

    header = {
        "Content-Type":"application/json",
        "Accept":"application/json",
        "Authorization":f"Bearer {airtable_api_key}"
    }

    data = {
        "fields": {
            "Finished project": confirm_project,
            "Working hours": work,
            "Interest": interest,
            "Difficulty": difficulty,
            "Assistance": assistance
        }
    }

    try:
        response = requests.post(
            request_url, headers=headers, data=json.dumps(data)
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return response
    print(response.status_code)

class HealthForm(FormAction):

    def name(self):
        return "health_form"

    @staticmethod
    def required_slots(tracker):
        return ["confirm_project", "work", "interest", "difficulty", "assistance"]

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
        response = create_health_log(
            tracker.get_slot("confirm_project"),
            tracker.get_slot("work"),
            tracker.get_slot("interest"),
            tracker.get_slot("difficulty"),
            tracker.get_slot("assistance"))

        # Send message to user that their answers have been recorder
        dispatcher.utter_message("Thanks, your answers have been recorded!")
        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "confirm_project": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
                self.from_intent(intent="inform", value=True),
            ],

            "work": [
                self.from_entity(entity="work"),
                self.from_intent(intent="deny", value="None"),
            ],

            "interest": [
                self.from_text(intent="inform"),
                self.from_text(intent="deny", value="None")
            ],

            "difficulty": [
                self.from_text(intent="inform"),
                self.from_text(intent="deny", value="None")
            ],

            "assistance": [
                self.from_text(intent="inform"),
                self.from_text(intent="deny", value="None")
            ]
        }